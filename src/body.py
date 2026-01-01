from drivePresenter import GoogleDrivePresenter
from flet import (
    Container,
    Colors
)

class Body(Container):
    def __init__(self):
        super().__init__()
        self.bgcolor = Colors.WHITE_10
        self.padding = 10

        self.systemLogic = GoogleDrivePresenter()
        self.width = self.systemLogic.BODY_MIN_WIDTH
        self.expand = True