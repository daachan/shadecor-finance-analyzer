from sidebar import Sidebar
from flet import (
    MouseCursor,
    Text
)

class SidebarView2(Sidebar):
    def __init__(self, func):
        super().__init__()
        
        # 1. クリック時の動作を登録
        self.on_click = lambda _: func("view1")
        
        # 2. ボタンとしての見た目のフィードバックを追加
        self.ink = True  # クリックした時に波紋が出る（Material Design風）
        self.mouse_cursor = MouseCursor.CLICK  # マウスが乗った時に指マークにする
        
        # コンテンツの配置（例）
        self.content = Text("ここをクリックすると遷移します")

    def baka(self):
        print("baka")