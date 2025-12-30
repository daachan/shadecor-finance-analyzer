from flet import (
    Container,
    Text,
    Colors,
    padding,
    Alignment,
    MouseCursor
)

class NameButton(Container):
    def __init__(self, name, func_switch):
        super().__init__()
        self.content = Text(name, size=16, color=Colors.BLACK)
        self.padding = padding.all(10)
        self.alignment = Alignment(-1.0, 0) 
        self.ink = True  
        self.mouse_cursor = MouseCursor.CLICK
        self.hover_color = Colors.BLUE_GREY_50
        self.bgcolor = Colors.WHITE
        self.border_radius = 10
        self.on_click = lambda _: self.clickHandle(name, func_switch) # クリック時に名前を渡す

    def clickHandle(self, name, func_swtich):
        #bodyを変える
        func_swtich(name)
        #自分自身の色を変更する


        
