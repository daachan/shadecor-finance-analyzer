from dotenv import load_dotenv
from datetime import datetime
import os
import pandas as pd
import glob

class GoogleDrivePresenter():
    def __init__(self):
        # 環境変数の読み込み
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        load_dotenv(env_path)

        self.SCRIPT_FOLDER_PATH = os.environ.get("SCRIPT_FOLDER_PATH")
        self.ERROR_FOLDER_PATH = os.environ.get("ERROR_FOLDER_PATH")
        self.NAME_FOLDER_PATH = os.environ.get("NAME_FOLDER_PATH")
        self.SIDEBAR_MIN_WIDTH = int(os.environ.get("SIDEBAR_MIN_WIDTH", 300))
        self.BODY_MIN_WIDTH = int(os.environ.get("BODY_MIN_WIDTH", 500))
        self.CONTENT_MIN_HEIGHT = int(os.environ.get("CONTENT_MIN_HEIGHT", 600))
    
    # マスタDBが存在しているか確認する
    def isDatasetExists(self, folder_path):
        if not folder_path:
            return False
        
        search = os.path.join(folder_path, "dataset*.csv")
        search_results = glob.glob(search)

        if not search_results:
            return False

        latest_masterdb_path = max(search_results, key=os.path.getmtime)
        return os.path.exists(latest_masterdb_path)
    
    # 指定フォルダに.xlsxファイルが存在するか確認する
    def hasErrorFiles(self, folder_path, extension=".xlsx"):
        if not folder_path or not os.path.exists(folder_path):
            return False

        datalist = os.listdir(folder_path)
        for data in datalist:
            fn, ex = os.path.splitext(data)
            if (ex == extension):
                return True

        return False

    # Driveに保存されているマスタデータを取得する
    def getDataset(self):
        search = os.path.join(str(self.SCRIPT_FOLDER_PATH), "dataset*.csv")
        search_results = glob.glob(search)

        lataset_masterdb_path = max(search_results, key=os.path.getmtime)

        sheet = pd.read_csv(lataset_masterdb_path)
        return sheet
    
    # 開始期間 ~ 終了期間までの対象.xlsxファイルを取得する
    # time入力形式 "YYYY-mm-dd" 
    def getXlsx(self, name:str, start_time:str, end_time:str):
        st = start_time + "_00-00-00"
        et = end_time + "_23-59-59"
        start_datetime = datetime.strptime(st, "%Y-%m-%d_%H-%M-%S")
        end_datetime = datetime.strptime(et, "%Y-%m-%d_%H-%M-%S")

        search = os.path.join(str(self.NAME_FOLDER_PATH), name + "*.xlsx")
        search_results = glob.glob(search)

        matched_file_path_list = [] 

        for data in search_results:
            file_name = os.path.basename(data)
            fn, ex = os.path.splitext(file_name)

            parts = fn.split("_")
            timestamp_str = f"{parts[1]}_{parts[2]}" # YY-mm-dd_HH-MM-SS
            timestamp_datetime = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")

            if start_datetime <= timestamp_datetime <= end_datetime:
                matched_file_path_list.append(data)
        
        return matched_file_path_list
    
    # 入力：中身を抽出したいファイルパスのリスト
    # 出力：["名前_申請日", "記入行ごとの情報", "記入行の金額"]
    def getExpenseData(self, file_path_list):
        # 申請書類の要素抽出
        transport_expense_list = []
        item_expense_list = []
        for path in file_path_list:
            #ファイル名に記載されている申請日を取得
            fn = os.path.basename(path)
            file_name, ex = os.path.splitext(fn)
            
            # .xlsxファイルの中身のデータ抜き出し
            df = pd.read_excel(path, header=None)
            # 交通費
            for r in range(11, 31):
                value = pd.to_numeric(df.iloc[r,14], errors='coerce') 
                if pd.isna(value):
                    break
                else:
                    transportation_type = str(df.iloc[r,1]) if pd.notna(df.iloc[r,1]) else "不明"
                    date_of_use = str(df.iloc[r,3])[:10] if pd.notna(df.iloc[r,3]) else "日時不詳"
                    departure_place = str(df.iloc[r,6]) if pd.notna(df.iloc[r,6]) else "不明"
                    arrival_place = str(df.iloc[r,9]) if pd.notna(df.iloc[r,9]) else "不明"
                    event_info = str(df.iloc[r,11]) if pd.notna(df.iloc[r,11]) else "不明"
                    tr_info = f"[{transportation_type}] {date_of_use}_[{departure_place}]-[{arrival_place}]区間_[{event_info}]"
                    transport_expense_list.append([file_name, tr_info, value])

            # 経費
            for r in range(34, 64):
                value = pd.to_numeric(df.iloc[r,14], errors='coerce')
                if pd.isna(value):
                    break
                else:
                    it_type = str(df.iloc[r,1]) if pd.notna(df.iloc[r,1]) else "不明"
                    purpose = str(df.iloc[r,3]) if pd.notna(df.iloc[r,3]) else ""
                    date_of_use_ = str(df.iloc[r,7])[:10] if pd.notna(df.iloc[r,7]) else "日時不明"
                    purchase_details = str(df.iloc[r,10]) if pd.notna(df.iloc[r,10]) else ""
                    it_info = f"[{it_type}] {date_of_use_}_用途(その他選択のみ)：{purpose} 詳細：{purchase_details}"
                    item_expense_list.append([file_name, it_info, value])

        print (transport_expense_list)
        print (item_expense_list)
        return transport_expense_list, item_expense_list







        

    
