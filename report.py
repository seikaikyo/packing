from fpdf import FPDF
import os

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Load NotoSerifTC font
pdf.add_font('NotoSerifTC', '', 'NotoSerifTC-VariableFont_wght.ttf', uni=True)  # 修改為 NotoSerifTC 字體的實際路徑
pdf.set_font('NotoSerifTC', '', 12)

# Title
pdf.cell(200, 10, txt="系統功能與統計報告", ln=True, align='C')

# Section 1: 功能分析
pdf.set_font('NotoSerifTC', '', 10)
pdf.ln(10)
pdf.cell(200, 10, txt="1. 功能分析", ln=True, align='L')

# Function to calculate word count
def count_words_in_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        return len(content.split())

# Paths to the script files
scripts = {
    "main.py": "main.py",
    "single.py": "single.py",
    "group.py": "group.py",
    "pallet_query.py": "pallet_query.py",
    "db_connect.py": "db_connect.py",
    "db_query.py": "db_query.py"
}

# Collecting word counts
word_counts = {}
for script_name, script_path in scripts.items():
    word_counts[script_name] = count_words_in_file(script_path)

# 1.1 main.py
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "1.1 main.py\n"
    "功能描述：這個文件是系統的入口點，提供了一個主頁面，允許用戶選擇不同的操作，如單片掃描、整組掃描和棧板查詢。"
    "它還會顯示 SQLite 和 MSSQL 的連線狀態，確保系統正常運行。\n"
    "主要功能：\n"
    "  - 連線狀態檢查與顯示（SQLite 和 MSSQL）。\n"
    "  - 選擇並啟動單片掃描、整組掃描、棧板查詢模塊。\n"
    "  - 界面簡潔，適合日常操作。\n"
))

# 1.2 single.py
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "1.2 single.py\n"
    "功能描述：處理單片掃描操作，允許用戶掃描單片產品序號，並自動將數據保存到本地 SQLite 和遠程 MSSQL 資料庫。該模塊還支持工單管理，包括清空輸入、關閉工單和數據匯出。\n"
    "主要功能：\n"
    "  - 單片產品掃描與序號管理。\n"
    "  - 本地與遠程資料庫的數據同步。\n"
    "  - 工單數據匯出為 Excel 文件。\n"
    "  - 清空資料庫與返回主頁功能。\n"
))

# 1.3 group.py
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "1.3 group.py\n"
    "功能描述：處理整組掃描操作，允許用戶掃描整組的母料與子料序號，並自動將數據保存到本地 SQLite 和遠程 MSSQL 資料庫。"
    "與單片掃描類似，該模塊支持工單管理和數據匯出。\n"
    "主要功能：\n"
    "  - 整組產品掃描（母料與子料）與序號管理。\n"
    "  - 本地與遠程資料庫的數據同步。\n"
    "  - 工單數據匯出為 Excel 文件。\n"
    "  - 清空資料庫與返回主頁功能。\n"
))

# 1.4 pallet_query.py
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "1.4 pallet_query.py\n"
    "功能描述：提供棧板查詢功能，允許用戶通過掃描產品序號來查詢其所屬的棧板號碼，並顯示該棧板上的所有產品序號。"
    "該功能有助於快速檢索包裝信息。\n"
    "主要功能：\n"
    "  - 基於產品序號的棧板號碼查詢。\n"
    "  - 顯示棧板上的所有產品序號。\n"
    "  - 返回主頁功能。\n"
))

# 1.5 db_connect.py
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "1.5 db_connect.py\n"
    "功能描述：負責資料庫連接的配置與建立，包含本地 SQLite 和遠程 MSSQL 資料庫的連接邏輯。該模塊為系統的數據存取提供基礎支持。\n"
    "主要功能：\n"
    "  - 本地 SQLite 資料庫的連接。\n"
    "  - 遠程 MSSQL 資料庫的連接。\n"
))

# 1.6 db_query.py
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "1.6 db_query.py\n"
    "功能描述：封裝了資料庫的查詢與操作語句，處理數據的插入、刪除、更新和查詢操作。"
    "該模塊集中管理所有與資料庫互動的邏輯。\n"
    "主要功能：\n"
    "  - 單片與整組掃描數據的插入與更新。\n"
    "  - 資料庫表的清空操作。\n"
    "  - 棧板號碼的查詢與數據提取。\n"
))

# Section 2: 統計分析
pdf.ln(10)
pdf.cell(200, 10, txt="2. 統計分析", ln=True, align='L')

# File and word counts statistics
total_files = len(word_counts)
total_words = sum(word_counts.values())

pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    f"總文件數: {total_files}\n"
    f"總字數: {total_words} 字\n\n"
    "各文件詳細統計:\n"
))

for script_name, word_count in word_counts.items():
    pdf.multi_cell(0, 10, txt=f"文件名: {script_name}, 字數: {word_count} 字\n")

# Save PDF
output_path = "系統功能與統計報告.pdf"
pdf.output(output_path)
