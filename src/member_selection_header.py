from member_selection_sidebar import MemberSelectionSidebar
from header import Header
from create_pdf import PDFGenerator
from flet import (
    IconButton,
    Icons,
    Colors,
    Page,
)

class MemberSelectionHeader(Header):
    def __init__(self, page: Page, sidebar: MemberSelectionSidebar):
        super().__init__()
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


        