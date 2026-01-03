from member_selection_sidebar import MemberSelectionSidebar
from create_pdf import PDFGenerator
from flet import (
    AppBar,
    MainAxisAlignment,
    CrossAxisAlignment,
    Colors,
    Page,
)

class Header(AppBar):
    def __init__(self):
        super().__init__()
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.START
        self.bgcolor = Colors.WHITE_10
        


        