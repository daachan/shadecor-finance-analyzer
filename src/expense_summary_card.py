from flet import (
    Container,
    Row,
    Text,
    TextOverflow,
    Colors,
    padding,
    Alignment,
    MouseCursor,
    Icon,
    Icons
)

class ExpenseSummaryCard(Container):
    def __init__(self, file_name, info, value):
        super().__init__()
        self.checkFrag = True
        self.file_name = file_name
        self.info = info
        self.value = value
        self.padding = padding.all(10)
        self.alignment = Alignment(-1.0, 0) 
        self.ink = True  
        self.mouse_cursor = MouseCursor.CLICK
        self.hover_color = Colors.BLUE_GREY_50
        self.bgcolor = Colors.WHITE
        self.border_radius = 10
        self.on_click = lambda _: self.clickHandle() # クリック時に名前を渡す

        self.content = Row(
            controls=[
                Icon(icon=Icons.RADIO_BUTTON_CHECKED if self.checkFrag else Icons.RADIO_BUTTON_OFF, color=Colors.AMBER),
                Text(
                    f"{self.file_name} {self.info} 金額：{self.value}円", 
                    size=8, 
                    color=Colors.BLACK,
                    max_lines=1,
                    expand=True
                )
            ]
        )

    def clickHandle(self):
        #自分自身の色を変更する
        if (self.checkFrag):
            self.checkFrag = False
        else:
            self.checkFrag = True

        #更新後のコンテンツ
        self.content = Row(
            controls=[
                Icon(icon=Icons.RADIO_BUTTON_CHECKED if self.checkFrag else Icons.RADIO_BUTTON_OFF, color=Colors.AMBER),
                Text(
                    f"{self.file_name} {self.info} 金額：{self.value}円",
                    size=8, 
                    color=Colors.BLACK,
                    max_lines=1,
                    expand=True
                )
            ]
        )
        
        self.page.update()