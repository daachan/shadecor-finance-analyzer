from sidebar import Sidebar
from flet import (
    MouseCursor,
    Text,
    Column,
    ScrollMode,
    Divider,
    Control
)

from name_button import NameButton

class SidebarView2(Sidebar):
    def __init__(self, func):
        super().__init__()
        
        db = self.systemLogic.getDataset()
        name_list = db["名前"].tolist()

        btn_list = []
        for name in name_list:
            btn = NameButton(name=name, func_switch=func)
            btn_list.append(btn)

        self.content = Column(
            controls=[
                Text("メンバーリスト", size=20),
                Divider(),  
                *btn_list,
            ],
            scroll=ScrollMode.AUTO, 
            spacing=5 
        )
        

    def baka(self):
        print("baka")