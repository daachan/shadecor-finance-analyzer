from member_selection_sidebar import MemberSelectionSidebar
from member_selection_body import MemberSelectionBody
from header import Header
from create_pdf import PDFGenerator
from flet import (
    IconButton,
    Icons,
    Colors,
    Page,
)

class MemberSelectionHeader(Header):
    def __init__(self, page: Page, sidebar: MemberSelectionSidebar, body_list: dict[str, MemberSelectionBody]):
        super().__init__()
        self.main_page = page
        self.sidebar = sidebar
        self.body_list = body_list
        
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

        selected_body_list : list[MemberSelectionBody] = []
        for name, body in self.body_list.items():
            if name in selected_namelist:
                selected_body_list.append(body)

        
        for name in selected_namelist:
            pdf = PDFGenerator(name, selected_body_list)
            pdf.create_pdf()


        