#必要ライブラリ読み込み
from flet import (
    Page,
    Row,
    MainAxisAlignment,
    CrossAxisAlignment,
    Container
)

#コンテンツ読み込み
from header import Header
from sidebar_view1 import SidebarView1
from sidebar_view2 import SidebarView2
from body_view1 import BodyView1
from body_view2 import BodyView2

#制御ロジック読み込み
from drivePresenter import GoogleDrivePresenter

#コンテンツ配置および遷移
class MyLayout(Row):
    def __init__(self, page: Page):
        super().__init__()
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.START

        #GoogleDrivePresenter
        systemLogic = GoogleDrivePresenter()

        if not systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH):
            print("dataset.csvが見つかりません")


        # print(systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH))
        # print(systemLogic.hasErrorFiles(systemLogic.ERROR_FOLDER_PATH))

        #初期状態の確認
        if (systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH)) and (not systemLogic.hasErrorFiles(systemLogic.ERROR_FOLDER_PATH)):
            print("view2に移行したよん")
        else:
            print("view1に移行したよん")

        #
        # page.add(Header())


    def changeView(self, view: str):
        if (view == "view1"):
            print("view1")
        elif (view == "view2"):
            print("view2")
        else:
            print("error")

