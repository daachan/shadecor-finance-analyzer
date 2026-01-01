from sidebar_view2 import SidebarView2
from create_pdf import PDFGenerator
from flet import (
    AppBar,
    MainAxisAlignment,
    CrossAxisAlignment,
    IconButton,
    Icons,
    Colors,
    Page,
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
        
        for name in selected_namelist:
            pdf = PDFGenerator(name)
            pdf.create_pdf()


        