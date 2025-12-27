from flet import (
    Row,
    MainAxisAlignment,
    CrossAxisAlignment
)

class Body(Row):
    def __init__(self):
        super().__init__()
        self.alignment=MainAxisAlignment.START
        self.vertical_alignment=CrossAxisAlignment.START