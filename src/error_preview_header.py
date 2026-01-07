from member_selection_sidebar import MemberSelectionSidebar
from header import Header
from create_pdf import PDFGenerator
from flet import (
    Page,
)

class ErrorPreviewHeader(Header):
    def __init__(self, page: Page):
        super().__init__()
        self.main_page = page
        

        