import sqlite3
import pyodbc

def connect_to_sqlite(db_name='packaging_data.db'):
    """建立並返回與本地 SQLite 資料庫的連接。"""
    conn = sqlite3.connect(db_name)
    return conn

def connect_to_mssql(server, database, username, password):
    """建立並返回與遠端 MSSQL 資料庫的連接。"""
    conn = pyodbc.connect(
        f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return conn
