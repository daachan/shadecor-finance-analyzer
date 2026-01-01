#必要ライブラリ読み込み
import sys
from flet import (
    Page,
    Row,
    MainAxisAlignment,
    CrossAxisAlignment,
    Container,
    Colors
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
        self.vertical_alignment=CrossAxisAlignment.STRETCH
        self.expand = True
        self.spacing = 0

        #GoogleDrivePresenter
        systemLogic = GoogleDrivePresenter()

        #コンテンツの最小サイズ設定
        page.window.min_width = systemLogic.SIDEBAR_MIN_WIDTH + systemLogic.BODY_MIN_WIDTH
        page.window.min_height = systemLogic.CONTENT_MIN_HEIGHT

        #基本レイアウト作成
        self.sidebar_container = SidebarView2(func=self.switchContentByName)
        self.body_container = BodyView1()

        page.appbar = Header(page, self.sidebar_container)
        self.controls = [
            self.sidebar_container,
            self.body_container
        ]

        if not systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH):
            print("dataset.csvが見つかりません")
            sys.exit()

        #初期状態の確認
        if (systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH)) and (not systemLogic.hasErrorFiles(systemLogic.ERROR_FOLDER_PATH)):
            print("view2に移行したよん")
        else:
            print("view1に移行したよん")
    
    #名前に応じたコンテンツを生成(view2 bodyの切り替え)
    def switchContentByName(self, pick_name: str):
        self.body_container = BodyView2(pick_name)
        self.controls = [
            self.sidebar_container,
            self.body_container
        ]
        self.update()


