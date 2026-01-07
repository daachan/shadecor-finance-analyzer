from sidebar import Sidebar
from flet import (
    Text,
    Column,
    ScrollMode,
    Divider,
)

from name_button import NameButton

class MemberSelectionSidebar(Sidebar):
    def __init__(self, func):
        super().__init__()
        
        db = self.systemLogic.getDataset()
        name_list = db["名前"].tolist()

        self.btn_list : list[NameButton] = []
        for name in name_list:
            btn = NameButton(name=name, func_switch=func)
            self.btn_list.append(btn)

        self.content = Column(
            controls=[
                Text("メンバーリスト", size=20),
                Divider(),  
                *self.btn_list,
            ],
            scroll=ScrollMode.AUTO, 
            spacing=5 
        )
        

    def baka(self):
        print("baka")