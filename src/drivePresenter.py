from dotenv import load_dotenv
import os

class GoogleDrivePresenter():
    def __init__(self):
        # 環境変数の読み込み
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        load_dotenv(env_path)

        self.SCRIPT_FOLDER_PATH = os.environ.get("SCRIPT_FOLDER_PATH")
        self.ERROR_FOLDER_PATH = os.environ.get("ERROR_FOLDER_PATH")
    
    # マスタDBが存在しているか確認する
    def isDatasetExists(self, folder_path):
        if not folder_path:
            return False
        
        masterdb_path = os.path.join(folder_path, "dataset.csv")
        return os.path.exists(masterdb_path)
    
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
