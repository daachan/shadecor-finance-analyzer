from flet import (
    AppBar,
    MainAxisAlignment,
    CrossAxisAlignment
)

class Header(AppBar):
    def __init__(self):
        super().__init__()
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.START