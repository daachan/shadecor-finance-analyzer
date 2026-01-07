from body import Body
from flet import (
    Alignment,
    Text
)

class ErrorPreviewBody(Body):
    def __init__(self, message:str):
        super().__init__()
        self.alignment = Alignment(0, 0)
        self.content = Text(message)
        print(message)
