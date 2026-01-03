from sidebar import Sidebar
from flet import (
    MouseCursor,
    Text
)

class ErrorPreviewSidebar(Sidebar):
    def __init__(self):
        super().__init__()
        
        print("エラー！")