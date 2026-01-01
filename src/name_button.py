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

class NameButton(Container):
    def __init__(self, name, func_switch):
        super().__init__()
        self.name = name
        self.checkFrag = False
        self.padding = padding.all(10)
        self.alignment = Alignment(-1.0, 0) 
        self.ink = True  
        self.mouse_cursor = MouseCursor.CLICK
        self.hover_color = Colors.BLUE_GREY_50
        self.bgcolor = Colors.WHITE
        self.border_radius = 10
        self.on_click = lambda _: self.clickHandle(func_switch) # クリック時に名前を渡す

        #初期ページ
        self.content = Row(
            controls=[
                Icon(icon=Icons.CHECK_BOX_OUTLINE_BLANK, color=Colors.AMBER),
                Text(
                    self.name, 
                    size=16, 
                    color=Colors.BLACK,
                    max_lines=1,
                    overflow=TextOverflow.ELLIPSIS,
                    expand=True
                )
            ]
        )

    def clickHandle(self, func_swtich):
        #bodyを変える
        func_swtich(self.name)

        #自分自身の色を変更する
        if (self.checkFrag):
            self.checkFrag = False
        else:
            self.checkFrag = True

        #更新後のコンテンツ
        self.content = Row(
            controls=[
                Icon(icon=Icons.CHECK_BOX_OUTLINE_BLANK if not self.checkFrag else Icons.CHECK_BOX, color=Colors.AMBER),
                Text(
                    self.name, 
                    size=16, 
                    color=Colors.BLACK,
                    max_lines=1,
                    overflow=TextOverflow.ELLIPSIS,
                    expand=True
                )
            ]
        )
        
        self.page.update()


        
