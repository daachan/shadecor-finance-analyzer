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
from member_selection_header import MemberSelectionHeader
from member_selection_sidebar import MemberSelectionSidebar
from member_selection_body import MemberSelectionBody
from error_preview_header import ErrorPreviewHeader
from error_preview_sidebar import ErrorPreviewSidebar
from error_preview_body import ErrorPreviewBody

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
        path_list, name_list = systemLogic.getXlsx("山田太郎", "2025-3-12", "2025-12-28")
        systemLogic.getExpenseData(path_list)

        #コンテンツの最小サイズ設定
        page.window.min_width = systemLogic.SIDEBAR_MIN_WIDTH + systemLogic.BODY_MIN_WIDTH
        page.window.min_height = systemLogic.CONTENT_MIN_HEIGHT

        #基本レイアウト作成
        self.sidebar_container = MemberSelectionSidebar(func=self.switchContentByName)
        self.body_container = ErrorPreviewBody("初期ページ")

        page.appbar = MemberSelectionHeader(page, self.sidebar_container)
        self.controls = [
            self.sidebar_container,
            self.body_container
        ]

        if not systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH):
            page.appbar = ErrorPreviewHeader(page)
            print("dataset.csvが見つかりません")

        #初期状態の確認
        if (systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH)) and (not systemLogic.hasErrorFiles(systemLogic.ERROR_FOLDER_PATH)):
            print("view2に移行したよん")
        else:
            print("view1に移行したよん")
    
    #名前に応じたコンテンツを生成(member_selection:bodyの切り替え)
    def switchContentByName(self, pick_name: str):
        self.body_container = MemberSelectionBody(pick_name)
        self.controls = [
            self.sidebar_container,
            self.body_container
        ]
        self.update()

    def occurError(self, main_page: Page, message: str):
            main_page.appbar = ErrorPreviewHeader(main_page)
            self.body_container = ErrorPreviewBody(message)
            self.sidebar_container = ErrorPreviewSidebar()


