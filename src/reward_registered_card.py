from flet import (
    Container,
    Row,
    Text,
    TextOverflow,
    TextAlign,
    KeyboardType,
    Colors,
    padding,
    Alignment,
    MouseCursor,
    IconButton,
    Icons,
    TextField,
    InputFilter
)

class RewardRegisteredCard(Container):
    def __init__(self, serial_num, func_delete):
        super().__init__()
        self.serial_num = serial_num
        self.padding = padding.all(10)
        self.alignment = Alignment(-1.0, 0) 
        self.ink = True  
        self.mouse_cursor = MouseCursor.CLICK
        self.hover_color = Colors.BLUE_GREY_50
        self.bgcolor = Colors.WHITE
        self.border_radius = 10

        def validate_number_input(e):
            # 入力欄が空、あるいは何も入力されていない場合に "0" を入れる
            if not e.control.value or e.control.value.strip() == "":
                e.control.value = "0"
                e.control.update()

        self.abstract_tb = TextField(
            label="摘要記入欄",
            hint_text="入力：5~10文字程度",
            multiline=False,
            max_lines=1,
            expand=3,
        )
        
        self.amount_tb = TextField(
            label="金額記入欄",
            value="0",
            multiline=False,
            max_lines=1,
            keyboard_type=KeyboardType.NUMBER,
            text_align=TextAlign.RIGHT,
            input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$"),
            on_blur=validate_number_input,
            expand=2,
        )

        self.content = Row(
            spacing=10,
            controls=[
                IconButton(icon=Icons.DELETE_FOREVER, on_click=lambda _ : func_delete(self.serial_num)),
                self.abstract_tb,
                self.amount_tb
            ]
        )

