from flet import (
    Container,
    Row,
    TextAlign,
    KeyboardType,
    Colors,
    padding,
    Alignment,
    MouseCursor,
    IconButton,
    Icons,
    TextField,
    InputFilter,
    Event
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

        # 入力値を保持しておく
        self.abstract : str = ""
        self.amount : int = 0

        def update_abstract(e:Event[TextField]):
            self.abstract = e.control.value

        def update_amount(e:Event[TextField]):
            # e.control.value が空文字 "" の場合は 0 を代入するようにガードをかける
            val = e.control.value
            if val == "" or val is None:
                self.amount = 0
            else:
                self.amount = int(val)

        # 入力欄が空、あるいは何も入力されていない場合に "0" を入れる
        def validate_number_input(e:Event[TextField]):
            if not e.control.value or e.control.value.strip() == "":
                e.control.value = "0"
                self.amount = 0
                e.control.update()
        
         # 入力欄が空、あるいは何も入力されていない場合に "" を入れる
        def validate_text_input(e:Event[TextField]):
            if not e.control.value or e.control.value.strip() == "":
                e.control.value = "未記入"
                self.abstract = "未記入"
                e.control.update()

        self.abstract_tb = TextField(
            label="摘要記入欄",
            hint_text="入力：5~10文字程度",
            value="未記入",
            multiline=False,
            max_lines=1,
            expand=3,
            on_blur=validate_text_input,
            on_change=lambda e:update_abstract(e)
        )
        
        self.amount_tb = TextField(
            label="金額記入欄",
            value="0",
            multiline=False,
            max_lines=1,
            keyboard_type=KeyboardType.NUMBER,
            text_align=TextAlign.RIGHT,
            input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$"),
            expand=2,
            on_blur=validate_number_input,
            on_change=lambda e:update_amount(e)
        )

        self.content = Row(
            spacing=10,
            controls=[
                IconButton(icon=Icons.DELETE_FOREVER, on_click=lambda _ : func_delete(self.serial_num)),
                self.abstract_tb,
                self.amount_tb
            ]
        )

