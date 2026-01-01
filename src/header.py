from create_pdf import ReportlabView
from name_button import NameButton
from sidebar_view2 import SidebarView2
from flet import (
    AppBar,
    MainAxisAlignment,
    CrossAxisAlignment,
    IconButton,
    Icons,
    Colors,
    Page,
    Text,
    AlertDialog
)

class Header(AppBar):
    def __init__(self, page: Page, sidebar: SidebarView2):
        super().__init__()
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.START
        self.bgcolor = Colors.WHITE_10
        self.main_page = page
        self.sidebar = sidebar
        
        self.actions=[
            IconButton(
                Icons.PRINT,
                icon_color=Colors.BLUE,
                tooltip="印刷する",
                on_click=lambda _: self.printHandle()
            ),
        ]

    def printHandle(self):
        selected_namelist = []
        for item in self.sidebar.btn_list:
            if item.checkFrag:
                selected_namelist.append(item.name)

        a = ReportlabView()

        