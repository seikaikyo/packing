# Packing Application

## English

This is a packing application developed using Python with Kivy for the user interface design. It supports both single item and group item scanning, and connects to both a local SQLite database and a remote MSSQL database.

### Features

- **Single Item Scanning**: Allows the user to scan individual product serial numbers and automatically save them to both the local SQLite and remote MSSQL databases.
- **Group Item Scanning**: Supports scanning of group items, including a master serial number and its associated child serial numbers, and saves them to the databases.
- **Pallet Query**: Users can scan a product serial number to query and display all items associated with the corresponding pallet number.
- **Real-time Database Connection Status**: Displays the connection status of both SQLite and MSSQL databases with a visual indicator.
- **Excel Export**: Allows exporting of scanned data to an Excel file with a filename based on the order number and timestamp.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/seikaikyo/packing.git
   cd packing
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the databases**:

   - Ensure you have SQLite and MSSQL set up.
   - Configure your MSSQL connection settings in `db_connect.py`.

5. **Run the application**:
   ```bash
   python main.py
   ```

### Usage

#### Single Item Scanning

- Navigate to the Single Item section.
- Enter the required information such as order number, station, and employee name.
- Scan the product serial number using a barcode scanner.
- The data will be automatically saved to the database.

#### Group Item Scanning

- Navigate to the Group Item section.
- Enter the master serial number and its associated child serial numbers.
- The data will be saved to the database as a group entry.

#### Pallet Query

- Navigate to the Pallet Query section.
- Scan a product serial number to retrieve and display the associated pallet information.

### Contributing

Feel free to fork this repository and contribute via pull requests. If you find any issues, please report them on the GitHub issue tracker.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contact

For any inquiries or support, please contact [Seikai Kyo](mailto:seikai.kyo@example.com).

---

## 日本語

これは、Kivy を使用してユーザーインターフェースを設計した Python で開発された梱包アプリケーションです。単一アイテムとグループアイテムのスキャンをサポートし、ローカルの SQLite データベースとリモートの MSSQL データベースの両方に接続します。

### 機能

- **単一アイテムのスキャン**: ユーザーが個々の製品シリアル番号をスキャンし、それをローカル SQLite データベースとリモート MSSQL データベースの両方に自動的に保存できるようにします。
- **グループアイテムのスキャン**: マスターシリアル番号とその関連する子シリアル番号を含むグループアイテムのスキャンをサポートし、データベースに保存します。
- **パレットクエリ**: ユーザーが製品シリアル番号をスキャンして対応するパレット番号に関連するすべてのアイテムを照会および表示できます。
- **リアルタイムデータベース接続ステータス**: SQLite と MSSQL のデータベース接続ステータスを視覚的なインジケーターで表示します。
- **Excel へのエクスポート**: スキャンされたデータを注文番号とタイムスタンプに基づいて命名された Excel ファイルにエクスポートできます。

### インストール

1. **リポジトリをクローンする**:

   ```bash
   git clone https://github.com/seikaikyo/packing.git
   cd packing
   ```

2. **仮想環境を設定する**（任意ですが推奨）:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows では `venv\Scripts\activate` を使用
   ```

3. **依存関係をインストールする**:

   ```bash
   pip install -r requirements.txt
   ```

4. **データベースを設定する**:

   - SQLite と MSSQL が設定されていることを確認します。
   - `db_connect.py` で MSSQL の接続設定を構成します。

5. **アプリケーションを実行する**:
   ```bash
   python main.py
   ```

### 使用法

#### 単一アイテムのスキャン

- 単一アイテムセクションに移動します。
- 注文番号、ステーション、および従業員名などの必要な情報を入力します。
- バーコードスキャナーを使用して製品シリアル番号をスキャンします。
- データは自動的にデータベースに保存されます。

#### グループアイテムのスキャン

- グループアイテムセクションに移動します。
- マスターシリアル番号とその関連する子シリアル番号を入力します。
- データはグループエントリとしてデータベースに保存されます。

#### パレットクエリ

- パレットクエリセクションに移動します。
- 製品シリアル番号をスキャンして、関連するパレット情報を取得および表示します。

### 貢献

このリポジトリをフォークして、プルリクエスト経由で貢献してください。問題が発生した場合は、GitHub の問題トラッカーに報告してください。

### ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

### 連絡先

質問やサポートについては、[Seikai Kyo](mailto:seikai.kyo@example.com) までご連絡ください。

---

## 正體中文

這是一個使用 Python 開發的包裝應用程式，使用 Kivy 進行用戶界面設計。它支援單品和組合項目掃描，並連接到本地 SQLite 資料庫和遠端 MSSQL 資料庫。

### 功能

- **單品掃描**：允許用戶掃描單個產品序號，並自動將其保存到本地 SQLite 資料庫和遠端 MSSQL 資料庫。
- **組合項目掃描**：支援掃描包含主序號和相關子序號的組合項目，並將數據保存到資料庫中。
- **棧板查詢**：用戶可以通過掃描產品序號來查詢並顯示與相應棧板號碼相關的所有項目。
- **實時資料庫連接狀態**：通過視覺指示器顯示 SQLite 和 MSSQL 資料庫的連接狀態。
- **Excel 匯出**：允許將掃描數據匯出為 Excel 文件，文件名基於訂單號碼和時間戳。

### 安裝

1. **克隆此存儲庫**：

   ```bash
   git clone https://github.com/seikaikyo/packing.git
   cd packing
   ```

2. **設置虛擬環境**（可選，但推薦）：

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows 系統使用 `venv\Scripts\activate`
   ```

3. **安裝依賴項**：

   ```bash
   pip install -r requirements.txt
   ```

4. **設置資料庫**：

   - 確保你已經設置了 SQLite 和 MSSQL。
   - 在 `db_connect.py` 中配置你的 MSSQL 連接設置。

5. **運行應用程式**：
   ```bash
   python main.py
   ```

### 使用方式

#### 單品掃描

- 導航到單品掃描部分。
- 輸入所需信息，如訂單號碼、工作站和員工名稱。
- 使用條碼掃描器掃描產品序號。
- 數據將自動保存到資料庫中。

#### 組合項目掃描

- 導航到組合項目部分。
- 輸入主序號及其相關的子序號。
- 數據將作為一個組合條目保存到資料庫中。

#### 棧板查詢

- 導航到棧板查詢部分。
- 掃描產品序號來檢索和顯示相關的棧板信息。

### 貢獻

歡迎 fork 此存儲庫並通過 pull request 進行貢獻。如果發現任何問題，請在 GitHub 問題追蹤器上報告。

### 許可證

此項目根據 MIT 許可證進行許可，詳細信息請參閱 [LICENSE](LICENSE) 文件。

### 聯絡方式

如有任何疑問或支持需求，請聯繫 [Seikai Kyo](mailto:seikai.kyo@example.com)。
