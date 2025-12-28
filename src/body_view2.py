from body import Body
from flet import (
    Alignment,
    Text
)

class BodyView2(Body):
    def __init__(self):
        super().__init__()
        self.alignment = Alignment(0, 0)
        self.content = Text("view2")

    def bakan(self):
        print("bakan")