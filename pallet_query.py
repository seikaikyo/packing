import tkinter as tk
from tkinter import messagebox
from db_query import DatabaseManager

class PalletQuery:
    def __init__(self, root):
        self.root = root
        self.root.title("棧板查詢")
        self.root.geometry("600x400")

        self.db = DatabaseManager()

        self.create_widgets()

    def create_widgets(self):
        font = ("Microsoft JhengHei", 12)

        # 置中框架
        center_frame = tk.Frame(self.root)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(center_frame, text="請刷讀產品序號:", font=font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.serial_entry = tk.Entry(center_frame, font=font, width=30)
        self.serial_entry.grid(row=0, column=1, padx=10, pady=10)
        self.serial_entry.bind('<Return>', self.query_pallet)

        self.result_label = tk.Label(center_frame, text="", font=font)
        self.result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.result_listbox = tk.Listbox(center_frame, width=60, height=10)
        self.result_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(center_frame, text="回到首頁", command=self.back_to_home, width=15, height=2).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def query_pallet(self, event=None):
        serial = self.serial_entry.get().strip()
        if not serial:
            messagebox.showwarning("輸入錯誤", "請輸入或掃描產品序號")
            return

        c = self.db.sqlite_conn.cursor()

        # 查詢單片
        c.execute("SELECT pallet_number FROM single_item WHERE serial_number = ?", (serial,))
        result = c.fetchone()

        if result:
            pallet_number = result[0]
            c.execute("SELECT serial_number FROM single_item WHERE pallet_number = ?", (pallet_number,))
            serials = c.fetchall()
            self.display_pallet_info(pallet_number, serials)
        else:
            # 查詢整組
            c.execute("SELECT pallet_number FROM group_item WHERE mother_serial = ? OR child_serial = ?", (serial, serial))
            result = c.fetchone()

            if result:
                pallet_number = result[0]
                c.execute("SELECT mother_serial, child_serial FROM group_item WHERE pallet_number = ?", (pallet_number,))
                serials = c.fetchall()
                self.display_pallet_info(pallet_number, serials, is_group=True)
            else:
                self.result_label.config(text="未找到對應的棧板", fg="red")
                self.result_listbox.delete(0, tk.END)

        self.serial_entry.delete(0, tk.END)

    def display_pallet_info(self, pallet_number, serials, is_group=False):
        self.result_label.config(text=f"棧板號碼: {pallet_number}", fg="green")
        self.result_listbox.delete(0, tk.END)

        for serial in serials:
            if is_group:
                self.result_listbox.insert(tk.END, f"母料: {serial[0]}, 子料: {serial[1]}")
            else:
                self.result_listbox.insert(tk.END, serial[0])

    def back_to_home(self):
        self.root.destroy()
        from main import HomePage
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()

def run_pallet_query():
    root = tk.Tk()
    app = PalletQuery(root)
    root.mainloop()

if __name__ == "__main__":
    run_pallet_query()
