import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import os
import pandas as pd

# 初始化資料庫
conn = sqlite3.connect('packaging_data.db')
c = conn.cursor()

# 創建資料表（如果不存在）
c.execute('''
CREATE TABLE IF NOT EXISTS single_item 
(order_number TEXT, station TEXT, employee TEXT, product_type TEXT, pallet_count INTEGER, serial_number TEXT UNIQUE, pallet_number TEXT, date TEXT, create_time TEXT)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS group_item 
(order_number TEXT, station TEXT, employee TEXT, product_type TEXT, pallet_count INTEGER, mother_serial TEXT, child_serial TEXT, pallet_number TEXT, date TEXT, create_time TEXT)
''')
conn.commit()

class BarcodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcode Scanner Input Interface")
        self.root.geometry("800x600")  # 設置寬度800，高度600
        
        self.create_widgets()
        self.order_entry.focus_set()  # 預設游標在工單號碼輸入欄位內
        self.pallet_serial_count = 0  # 用於計算產品序號數量
        self.current_pallet_number = None
        self.pallet_sequence = 1  # 每日棧板號碼的序列
        self.mother_serial = None  # 整組的母料序號
        self.children_count = 0  # 記錄當前母料已經輸入的子料數量

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
        
        # 產品規格選項
        tk.Label(self.root, text="產品規格:", font=font).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.spec_var = tk.StringVar(value="單(17)")
        self.spec_var.trace('w', self.update_spec_options)
        
        # 單片選項
        self.single_frame = tk.Frame(self.root)
        self.single_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        single_specs = ["單(17)", "單(27)", "單(16)", "單(26)", "單(15)", "單(25)"]
        for i, spec in enumerate(single_specs):
            tk.Radiobutton(self.single_frame, text=spec, variable=self.spec_var, value=spec, font=font).grid(row=i//3, column=i%3, sticky="w")

        # 整組選項
        self.comb_frame = tk.Frame(self.root)
        self.comb_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        comb_specs = ["整組(14)", "整組(24)"]
        for i, spec in enumerate(comb_specs):
            tk.Radiobutton(self.comb_frame, text=spec, variable=self.spec_var, value=spec, font=font).grid(row=i, column=0, sticky="w")

        tk.Label(self.root, text="棧板數量:", font=font).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.pallet_count_entry = tk.Entry(self.root, font=font, width=20)
        self.pallet_count_entry.grid(row=5, column=1, padx=10, pady=10)
        self.pallet_count_entry.bind('<Return>', self.focus_next_widget)

        # 單片的產品序號輸入框
        self.serial_label = tk.Label(self.root, text="產品序號:", font=font)
        self.serial_entry = tk.Entry(self.root, font=font, width=20)
        self.serial_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.serial_entry.grid(row=6, column=1, padx=10, pady=10)
        self.serial_entry.bind('<Return>', self.add_serial)

        self.serial_listbox = tk.Listbox(self.root)
        self.serial_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        
        self.count_label = tk.Label(self.root, text="目前包裝數量: 0")
        self.count_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(button_frame, text="清空", command=self.clear_entries).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="關閉工單", command=self.close_order).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="清空資料庫", command=self.clear_database).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="匯出 EXCEL", command=self.export_to_excel).grid(row=0, column=3, padx=5, pady=5)

        # 整組母料與子料選項
        self.group_option_frame = tk.Frame(self.root)
        self.group_option_frame.grid(row=0, column=2, rowspan=10, padx=10, pady=10, sticky="n")

        self.carton_var = tk.StringVar(value="1:2")
        self.carton_1_2 = tk.Radiobutton(self.group_option_frame, text="CARTON 1:2", variable=self.carton_var, value="1:2", font=font, command=self.update_group_options)
        self.carton_1_4 = tk.Radiobutton(self.group_option_frame, text="CARTON 1:4", variable=self.carton_var, value="1:4", font=font, command=self.update_group_options)

        self.carton_1_2.grid(row=0, column=0, padx=10, pady=5)
        self.carton_1_4.grid(row=0, column=1, padx=10, pady=5)

        self.mother_label = tk.Label(self.group_option_frame, text="母料:", font=font)
        self.mother_entry = tk.Entry(self.group_option_frame, font=font, width=20)
        self.mother_entry.bind('<Return>', self.focus_next_widget)
        self.child_labels = [tk.Label(self.group_option_frame, text=f"子料{i+1}:", font=font) for i in range(4)]
        self.child_entries = [tk.Entry(self.group_option_frame, font=font, width=20) for i in range(4)]
        for entry in self.child_entries:
            entry.bind('<Return>', self.focus_next_widget)

        self.update_spec_options()

    def update_spec_options(self, *args):
        if self.spec_var.get().startswith("整組"):
            self.serial_label.grid_remove()
            self.serial_entry.grid_remove()
            self.group_option_frame.grid()
            self.carton_var.set("1:2")
            self.update_group_options()
        else:
            self.group_option_frame.grid_remove()
            self.serial_label.grid()
            self.serial_entry.grid()

    def update_group_options(self):
        if self.carton_var.get() == "1:2":
            self.mother_label.grid(row=1, column=0, padx=10, pady=5)
            self.mother_entry.grid(row=1, column=1, padx=10, pady=5)
            for i in range(2):
                self.child_labels[i].grid(row=i+2, column=0, padx=10, pady=5)
                self.child_entries[i].grid(row=i+2, column=1, padx=10, pady=5)
            for i in range(2, 4):
                self.child_labels[i].grid_remove()
                self.child_entries[i].grid_remove()
        else:
            self.mother_label.grid(row=1, column=0, padx=10, pady=5)
            self.mother_entry.grid(row=1, column=1, padx=10, pady=5)
            for i in range(4):
                self.child_labels[i].grid(row=i+2, column=0, padx=10, pady=5)
                self.child_entries[i].grid(row=i+2, column=1, padx=10, pady=5)

    def clear_entries(self):
        self.order_entry.delete(0, tk.END)
        self.station_entry.delete(0, tk.END)
        self.employee_entry.delete(0, tk.END)
        self.spec_var.set("單(17)")
        self.pallet_count_entry.delete(0, tk.END)
        self.serial_entry.delete(0, tk.END)
        self.serial_listbox.delete(0, tk.END)
        self.mother_entry.delete(0, tk.END)
        for entry in self.child_entries:
            entry.delete(0, tk.END)
        self.update_count()
        self.pallet_serial_count = 0
        self.current_pallet_number = None
        self.mother_serial = None
        self.children_count = 0
        self.order_entry.focus_set()

    def clear_database(self):
        if messagebox.askokcancel("清空資料庫", "確定要清空資料庫嗎？這將刪除所有資料。"):
            c.execute('DELETE FROM single_item')
            c.execute('DELETE FROM group_item')
            conn.commit()
            messagebox.showinfo("資料庫清空", "資料庫已清空。")

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def add_serial(self, event=None):
        serial = self.serial_entry.get()
        order = self.order_entry.get()
        pallet_count = int(self.pallet_count_entry.get() or 0)
        product_type = self.spec_var.get()

        if product_type.startswith("整組"):
            mother_serial = self.mother_entry.get()
            child_serials = [entry.get() for entry in self.child_entries if entry.get()]
            if not mother_serial or len(child_serials) != (2 if self.carton_var.get() == "1:2" else 4):
                messagebox.showwarning("輸入錯誤", "請填寫完整的母料和子料")
                return

            self.insert_serial(mother_serial, order, pallet_count, is_mother=True, is_single=False)
            for child_serial in child_serials:
                self.insert_serial(child_serial, order, pallet_count, is_mother=False, is_single=False)

        else:
            if serial:
                self.insert_serial(serial, order, pallet_count, is_mother=False, is_single=True)

    def insert_serial(self, serial, order, pallet_count, is_mother, is_single):
        if is_single:
            # 單片處理
            c.execute('SELECT COUNT(*) FROM single_item WHERE serial_number = ?', (serial,))
            if c.fetchone()[0] > 0:
                messagebox.showwarning("輸入錯誤", f"單片序號 {serial} 已存在，無法重複使用")
                self.serial_entry.delete(0, tk.END)
                return
            self.save_to_database_single(serial)
        else:
            if is_mother:
                # 檢查母料序號是否已經存在於 group_item 表中
                c.execute('SELECT COUNT(*) FROM group_item WHERE mother_serial = ?', (serial,))
                if c.fetchone()[0] > 0:
                    messagebox.showwarning("輸入錯誤", f"母料序號 {serial} 已存在，無法重複使用")
                    return
                self.mother_serial = serial
            else:
                # 檢查子料序號是否已經存在於 group_item 表中
                c.execute('SELECT COUNT(*) FROM group_item WHERE child_serial = ?', (serial,))
                if c.fetchone()[0] > 0:
                    messagebox.showwarning("輸入錯誤", f"子料序號 {serial} 已存在，無法重複使用")
                    return
            self.save_to_database_group(serial, is_mother)

        if serial not in self.serial_listbox.get(0, tk.END):
            self.serial_listbox.insert(tk.END, serial)
            self.serial_entry.delete(0, tk.END)
            self.update_count()
            self.pallet_serial_count += 1
            if self.pallet_serial_count == pallet_count:
                self.generate_new_pallet_number()  # 更新條件為等於
                self.pallet_serial_count = 0  # 重置計數
        else:
            self.serial_entry.delete(0, tk.END)

    def update_count(self):
        count = self.serial_listbox.size()
        self.count_label.config(text=f"目前包裝數量: {count}")

    def generate_new_pallet_number(self):
        today = datetime.now().strftime("%Y%m%d")
        self.current_pallet_number = f"{today}{self.pallet_sequence:03d}"
        self.pallet_sequence += 1

    def save_to_database_single(self, serial):
        if self.current_pallet_number is None:
            self.generate_new_pallet_number()

        order = self.order_entry.get()
        station = self.station_entry.get()
        employee = self.employee_entry.get()
        pallet_count = int(self.pallet_count_entry.get() or 0)
        product_type = self.spec_var.get()
        date = datetime.now().strftime("%Y-%m-%d")
        create_time = datetime.now().strftime("%H:%M:%S")

        c.execute('''
        INSERT INTO single_item (order_number, station, employee, product_type, pallet_count, serial_number, pallet_number, date, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order, station, employee, product_type, pallet_count, serial, self.current_pallet_number, date, create_time))
        
        conn.commit()

    def save_to_database_group(self, serial, is_mother):
        if self.current_pallet_number is None:
            self.generate_new_pallet_number()

        order = self.order_entry.get()
        station = self.station_entry.get()
        employee = self.employee_entry.get()
        pallet_count = int(self.pallet_count_entry.get() or 0)
        product_type = self.spec_var.get()
        date = datetime.now().strftime("%Y-%m-%d")
        create_time = datetime.now().strftime("%H:%M:%S")

        if is_mother:
            c.execute('''
            INSERT INTO group_item (order_number, station, employee, product_type, pallet_count, mother_serial, child_serial, pallet_number, date, create_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (order, station, employee, product_type, pallet_count, serial, None, self.current_pallet_number, date, create_time))
        else:
            c.execute('''
            INSERT INTO group_item (order_number, station, employee, product_type, pallet_count, mother_serial, child_serial, pallet_number, date, create_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (order, station, employee, product_type, pallet_count, self.mother_serial, serial, self.current_pallet_number, date, create_time))
        
        conn.commit()

    def close_order(self):
        order = self.order_entry.get()
        if not order:
            messagebox.showwarning("輸入錯誤", "請先輸入工單號碼")
            return

        self.export_to_excel()
        self.clear_entries()

    def show_summary_popup(self, order, station, employee, total):
        popup = tk.Toplevel(self.root)
        popup.title("工單總結")

        msg = f"工單號碼: {order}\n包裝工站: {station}\n包裝人員: {employee}\n總共包裝數量: {total}\n感謝您今天的付出，辛苦了。"
        self.summary_text = tk.Text(popup, width=40, height=10)
        self.summary_text.insert(tk.END, msg)
        self.summary_text.pack(padx=10, pady=10)

        popup.after(5000, popup.destroy)

    def export_to_excel(self):
        order = self.order_entry.get()
        if not order:
            messagebox.showwarning("輸入錯誤", "請先輸入工單號碼")
            return

        single_query = "SELECT * FROM single_item WHERE order_number = ?"
        group_query = "SELECT * FROM group_item WHERE order_number = ?"
        
        single_df = pd.read_sql_query(single_query, conn, params=(order,))
        group_df = pd.read_sql_query(group_query, conn, params=(order,))
        
        if single_df.empty and group_df.empty:
            messagebox.showwarning("無資料", "無此工單號碼的資料")
            return

        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        filename = f"{order}_{timestamp}.xlsx"
        filepath = os.path.join(os.getcwd(), filename)
        
        with pd.ExcelWriter(filepath) as writer:
            single_df.to_excel(writer, sheet_name='Single Items', index=False)
            group_df.to_excel(writer, sheet_name='Group Items', index=False)
        
        messagebox.showinfo("匯出成功", f"資料已匯出至 {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeScannerApp(root)
    root.mainloop()
