from dotenv import load_dotenv
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

    def getDataset(self):
        search = os.path.join(str(self.SCRIPT_FOLDER_PATH), "dataset*.csv")
        search_results = glob.glob(search)

        lataset_masterdb_path = max(search_results, key=os.path.getmtime)

        sheet = pd.read_csv(lataset_masterdb_path)
        return sheet

    
