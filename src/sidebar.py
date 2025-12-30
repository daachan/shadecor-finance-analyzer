from drivePresenter import GoogleDrivePresenter
from flet import (
    Container,
    Colors
)

class Sidebar(Container):
    def __init__(self):
        super().__init__()
        self.bgcolor = Colors.BLUE_50
        self.padding = 10

        self.systemLogic = GoogleDrivePresenter()
        self.width = self.systemLogic.SIDEBAR_MIN_WIDTH
        self.expand = False