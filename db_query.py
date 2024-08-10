from db_connect import connect_to_sqlite, connect_to_mssql

class DatabaseManager:
    def __init__(self, sqlite_db='packaging_data.db', mssql_config=None):
        self.sqlite_conn = connect_to_sqlite(sqlite_db)
        self.mssql_conn = None
        if mssql_config:
            self.mssql_conn = connect_to_mssql(
                server=mssql_config['server'],
                database=mssql_config['database'],
                username=mssql_config['username'],
                password=mssql_config['password']
            )

    def create_tables(self):
        """創建資料表（如果不存在）"""
        c = self.sqlite_conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS single_item 
        (order_number TEXT, station TEXT, employee TEXT, product_type TEXT, pallet_count INTEGER, 
        serial_number TEXT UNIQUE, pallet_number TEXT, date TEXT, create_time TEXT)
        ''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS group_item 
        (order_number TEXT, station TEXT, employee TEXT, product_type TEXT, pallet_count INTEGER, 
        mother_serial TEXT, child_serial TEXT, pallet_number TEXT, date TEXT, create_time TEXT)
        ''')
        self.sqlite_conn.commit()

    def insert_single_item(self, data):
        """插入單片項目至 SQLite 資料庫。"""
        c = self.sqlite_conn.cursor()
        c.execute('''
        INSERT INTO single_item (order_number, station, employee, product_type, pallet_count, 
        serial_number, pallet_number, date, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.sqlite_conn.commit()

    def insert_group_item(self, data):
        """插入整組項目至 SQLite 資料庫。"""
        c = self.sqlite_conn.cursor()
        c.execute('''
        INSERT INTO group_item (order_number, station, employee, product_type, pallet_count, 
        mother_serial, child_serial, pallet_number, date, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.sqlite_conn.commit()

    def sync_to_mssql(self):
        """將 SQLite 中的資料同步到 MSSQL。"""
        if not self.mssql_conn:
            print("MSSQL 連接未設定。")
            return

        # 將同步邏輯實作在這裡
        # 可以使用 SELECT 從 SQLite 讀取資料，然後插入 MSSQL
        pass

    def clear_table(self, table_name):
        """清空指定的資料表。"""
        c = self.sqlite_conn.cursor()
        c.execute(f'DELETE FROM {table_name}')
        self.sqlite_conn.commit()
