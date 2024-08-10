import tkinter as tk
from db_connect import connect_to_sqlite, connect_to_mssql

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("選擇功能")
        self.root.geometry("700x150")

        # 建立框架以便整齊排列元件
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)

        # 連線狀態標籤
        self.sqlite_status_label = tk.Label(status_frame, text="SQLite: 檢查中...", width=25, height=2)
        self.sqlite_status_label.grid(row=0, column=0, padx=10)

        self.mssql_status_label = tk.Label(status_frame, text="MSSQL: 檢查中...", width=25, height=2)
        self.mssql_status_label.grid(row=0, column=1, padx=10)

        # 功能選擇按鈕框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="單片", command=self.open_single_function, width=20, height=3).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="整組", command=self.open_group_function, width=20, height=3).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="棧板查詢", command=self.open_pallet_query, width=20, height=3).grid(row=0, column=2, padx=10)

        # 檢查連線狀態
        self.check_connections()

    def check_connections(self):
        # 檢查 SQLite 連線
        try:
            sqlite_conn = connect_to_sqlite()
            if sqlite_conn:
                self.sqlite_status_label.config(text="SQLite: 連線正常", bg="green", fg="white")
            else:
                self.sqlite_status_label.config(text="SQLite: 連線失敗", bg="red", fg="white")
        except Exception as e:
            self.sqlite_status_label.config(text="SQLite: 連線失敗", bg="red", fg="white")

        # 檢查 MSSQL 連線
        try:
            mssql_conn = connect_to_mssql()
            if mssql_conn:
                self.mssql_status_label.config(text="MSSQL: 連線正常", bg="green", fg="white")
            else:
                self.mssql_status_label.config(text="MSSQL: 連線失敗", bg="red", fg="white")
        except Exception as e:
            self.mssql_status_label.config(text="MSSQL: 連線失敗", bg="red", fg="white")

    def open_single_function(self):
        self.root.destroy()
        import single
        single.run_single_function()

    def open_group_function(self):
        self.root.destroy()
        import group
        group.run_group_function()

    def open_pallet_query(self):
        self.root.destroy()
        import pallet_query
        pallet_query.run_pallet_query()

if __name__ == "__main__":
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
