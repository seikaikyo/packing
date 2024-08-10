import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import pandas as pd
from db_query import DatabaseManager

class SingleFunction:
    def __init__(self, root):
        self.root = root
        self.root.title("單片掃描介面")
        self.root.geometry("800x600")

        self.db = DatabaseManager()
        self.db.create_tables()

        self.create_widgets()

    def create_widgets(self):
        font = ("Microsoft JhengHei", 12)

        tk.Label(self.root, text="工單:", font=font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.order_entry = tk.Entry(self.root, font=font, width=20)
        self.order_entry.grid(row=0, column=1, padx=10, pady=10)
        self.order_entry.bind('<Return>', self.focus_next_widget)
        
        tk.Label(self.root, text="包裝工站:", font=font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.station_entry = tk.Entry(self.root, font=font, width=20)
        self.station_entry.grid(row=1, column=1, padx=10, pady=10)
        self.station_entry.bind('<Return>', self.focus_next_widget)
        
        tk.Label(self.root, text="包裝員工:", font=font).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.employee_entry = tk.Entry(self.root, font=font, width=20)
        self.employee_entry.grid(row=2, column=1, padx=10, pady=10)
        self.employee_entry.bind('<Return>', self.focus_next_widget)
        
        tk.Label(self.root, text="產品規格:", font=font).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.spec_var = tk.StringVar(value="單(17)")
        single_specs = ["單(17)", "單(27)", "單(16)", "單(26)", "單(15)", "單(25)"]
        self.single_frame = tk.Frame(self.root)
        self.single_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        for i, spec in enumerate(single_specs):
            tk.Radiobutton(self.single_frame, text=spec, variable=self.spec_var, value=spec, font=font).grid(row=i//3, column=i%3, sticky="w")

        tk.Label(self.root, text="棧板數量:", font=font).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.pallet_count_entry = tk.Entry(self.root, font=font, width=20)
        self.pallet_count_entry.grid(row=4, column=1, padx=10, pady=10)
        self.pallet_count_entry.bind('<Return>', self.focus_next_widget)
        
        tk.Label(self.root, text="產品序號:", font=font).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.serial_entry = tk.Entry(self.root, font=font, width=20)
        self.serial_entry.grid(row=5, column=1, padx=10, pady=10)
        self.serial_entry.bind('<Return>', self.add_serial)

        self.serial_listbox = tk.Listbox(self.root)
        self.serial_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        self.count_label = tk.Label(self.root, text="目前包裝數量: 0")
        self.count_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(button_frame, text="清空", command=self.clear_entries).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="關閉工單", command=self.close_order).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="清空資料庫", command=self.clear_database).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="匯出 EXCEL", command=self.export_to_excel).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="回到首頁", command=self.back_to_home).grid(row=0, column=4, padx=5, pady=5)

        self.pallet_serial_count = 0
        self.current_pallet_number = None
        self.pallet_sequence = 1  # 每日棧板號碼的序列

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def add_serial(self, event=None):
        serial = self.serial_entry.get()
        order = self.order_entry.get()
        pallet_count = int(self.pallet_count_entry.get() or 0)

        if serial:
            self.insert_serial(serial, order, pallet_count)

    def insert_serial(self, serial, order, pallet_count):
        c = self.db.sqlite_conn.cursor()
        c.execute('SELECT COUNT(*) FROM single_item WHERE serial_number = ?', (serial,))
        if c.fetchone()[0] > 0:
            messagebox.showwarning("輸入錯誤", f"單片序號 {serial} 已存在，無法重複使用")
            self.serial_entry.delete(0, tk.END)
            return
        
        self.save_to_database(serial)

        if serial not in self.serial_listbox.get(0, tk.END):
            self.serial_listbox.insert(tk.END, serial)
            self.serial_entry.delete(0, tk.END)
            self.update_count()
            self.pallet_serial_count += 1
            if self.pallet_serial_count == pallet_count:
                self.generate_new_pallet_number()
                self.pallet_serial_count = 0
        else:
            self.serial_entry.delete(0, tk.END)

    def update_count(self):
        count = self.serial_listbox.size()
        self.count_label.config(text=f"目前包裝數量: {count}")

    def generate_new_pallet_number(self):
        today = datetime.now().strftime("%Y%m%d")
        self.current_pallet_number = f"{today}{self.pallet_sequence:03d}"
        self.pallet_sequence += 1

    def save_to_database(self, serial):
        if self.current_pallet_number is None:
            self.generate_new_pallet_number()

        order = self.order_entry.get()
        station = self.station_entry.get()
        employee = self.employee_entry.get()
        pallet_count = int(self.pallet_count_entry.get() or 0)
        product_type = self.spec_var.get()
        date = datetime.now().strftime("%Y-%m-%d")
        create_time = datetime.now().strftime("%H:%M:%S.%f")  # 包含毫秒的時間戳

        data = (order, station, employee, product_type, pallet_count, serial, self.current_pallet_number, date, create_time)
        self.db.insert_single_item(data)

    def clear_entries(self):
        self.order_entry.delete(0, tk.END)
        self.station_entry.delete(0, tk.END)
        self.employee_entry.delete(0, tk.END)
        self.spec_var.set("單(17)")
        self.pallet_count_entry.delete(0, tk.END)
        self.serial_entry.delete(0, tk.END)
        self.serial_listbox.delete(0, tk.END)
        self.update_count()
        self.pallet_serial_count = 0
        self.current_pallet_number = None
        self.order_entry.focus_set()

    def clear_database(self):
        if messagebox.askokcancel("清空資料庫", "確定要清空資料庫嗎？這將刪除所有資料。"):
            self.db.clear_table('single_item')
            messagebox.showinfo("資料庫清空", "資料庫已清空。")

    def close_order(self):
        order = self.order_entry.get()
        if not order:
            messagebox.showwarning("輸入錯誤", "請先輸入工單號碼")
            return

        self.export_to_excel()
        self.clear_entries()

    def export_to_excel(self):
        order = self.order_entry.get()
        if not order:
            messagebox.showwarning("輸入錯誤", "請先輸入工單號碼")
            return

        single_query = "SELECT * FROM single_item WHERE order_number = ?"
        single_df = pd.read_sql_query(single_query, self.db.sqlite_conn, params=(order,))
        
        if single_df.empty:
            messagebox.showwarning("無資料", "無此工單號碼的資料")
            return

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{order}_{timestamp}.xlsx"
        filepath = os.path.join(os.getcwd(), filename)
        
        with pd.ExcelWriter(filepath) as writer:
            single_df.to_excel(writer, sheet_name='Single Items', index=False)
        
        messagebox.showinfo("匯出成功", f"資料已匯出至 {filename}")

    def back_to_home(self):
        self.root.destroy()
        from main import HomePage  # 在這裡進行導入
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()

def run_single_function():
    root = tk.Tk()
    app = SingleFunction(root)
    root.mainloop()

if __name__ == "__main__":
    run_single_function()
