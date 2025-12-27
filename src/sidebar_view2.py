from sidebar import Sidebar
from flet import (
    Column,
    MainAxisAlignment,
    CrossAxisAlignment
)

class SidebarView2(Sidebar):
    def __init__(self):
        super().__init__()

    def baka(self):
        print("baka")