from flet import (
    Row,
    CrossAxisAlignment,
    Colors,
)

class Box(Row):
    def __init__(self):
        super().__init__()
        self.height=300
        self.vertical_alignment=CrossAxisAlignment.STRETCH
        self.box_color = Colors.GREEN_50
        self.box_padding = 5
        

    
