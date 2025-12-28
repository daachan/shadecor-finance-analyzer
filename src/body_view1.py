from body import Body
from flet import (
    Alignment,
    Text
)

class BodyView1(Body):
    def __init__(self):
        super().__init__()
        self.alignment = Alignment(0, 0)
        self.content = Text("view1")

    def ahoi(self):
        print("ahoi")