from flet import (
    Column,
    MainAxisAlignment,
    CrossAxisAlignment
)

class Sidebar(Column):
    def __init__(self):
        super().__init__()
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.START