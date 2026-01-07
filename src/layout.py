#必要ライブラリ読み込み
from flet import (
    Page,
    Row,
    MainAxisAlignment,
    CrossAxisAlignment,
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
        self.main_page = page
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.STRETCH
        self.expand = True
        self.spacing = 0

        #GoogleDrivePresenter
        systemLogic = GoogleDrivePresenter()
        path_list = systemLogic.getXlsx("山田太郎", "2025-3-12", "2025-12-28")
        systemLogic.getExpenseData(path_list)

        #呼び出すbodyインスタンスの辞書を作成
        self.member_body_instances = {}

        #コンテンツの最小サイズ設定
        page.window.min_width = systemLogic.SIDEBAR_MIN_WIDTH + systemLogic.BODY_MIN_WIDTH
        page.window.min_height = systemLogic.CONTENT_MIN_HEIGHT

        #基本レイアウト作成
        self.sidebar_container = MemberSelectionSidebar(func=self.switchContentByName)
        self.body_container = ErrorPreviewBody("")
        page.appbar = MemberSelectionHeader(page, self.sidebar_container, self.member_body_instances)

        #初期状態の確認
        if not systemLogic.isDatasetExists(systemLogic.SCRIPT_FOLDER_PATH):
            self.occurError("ERROR:dataset.csvが見つかりません")

        if systemLogic.hasErrorFiles(systemLogic.ERROR_FOLDER_PATH):
            self.occurError("ERROR:退避用フォルダの中身を移行/削除してください")
        
        self.controls = [
            self.sidebar_container,
            self.body_container
        ]
    
    #名前に応じたコンテンツを生成(member_selection:bodyの切り替え)
    def switchContentByName(self, pick_name: str):
        if pick_name not in self.member_body_instances: #既存のインスタンスが存在しなければ新規作成
            self.member_body_instances[pick_name] = MemberSelectionBody(pick_name)

        self.body_container = self.member_body_instances[pick_name]

        self.controls = [
            self.sidebar_container,
            self.body_container
        ]
        self.update()

    def occurError(self, message: str):
            self.main_page.appbar = ErrorPreviewHeader(self.main_page)
            self.body_container = ErrorPreviewBody(message)
            self.sidebar_container = ErrorPreviewSidebar()


