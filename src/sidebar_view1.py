from sidebar import Sidebar
from flet import (
    Column,
    MainAxisAlignment,
    CrossAxisAlignment
)

class SidebarView1(Sidebar):
    def __init__(self):
        super().__init__()

    def aho(self):
        print("aho")