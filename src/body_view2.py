from body import Body
from flet import (
    Column,
    Row,
    Container,
    Text,
    Divider,
    VerticalDivider,
    CrossAxisAlignment,
    MainAxisAlignment,
    Colors
)

class BodyView2(Body):
    def __init__(self, name: str):
        super().__init__()
        
        db = self.systemLogic.getDataset()
        member_data = db.loc[db["名前"] == name]

        self.content = Column(
            spacing=5,
            controls=[
                Text(member_data.iloc[0]["名前"], size=32),
                Divider(color=Colors.BLACK),
                Text("職位：" + member_data.iloc[0]["職位"], size=12),
                Text("学籍番号：" + str(member_data.iloc[0]["学籍番号"]), size=12),
                Container(height=10),
                Container(
                    height=120, #verticalDividerの長さ
                    content=Row(
                        spacing=20,
                        vertical_alignment=CrossAxisAlignment.STRETCH,
                        controls=[
                            Column(
                                controls=[
                                    Text("出席（オンライン含む）：" + str(member_data.iloc[0]["出席（オンライン含む）"]), size=12),
                                    Text("出張：" + str(member_data.iloc[0]["出張"]), size=12),
                                    Text("欠席：" + str(member_data.iloc[0]["欠席"]), size=12),
                                    Text("遅刻：" + str(member_data.iloc[0]["遅刻"]), size=12),
                                ]
                            ),
                            VerticalDivider(width=1, thickness=1, color=Colors.BLACK),
                            Column(
                                controls=[
                                    Text("現場回数：" + str(member_data.iloc[0]["現場回数"]), size=12),
                                    Text("Top Duty回数：" + str(member_data.iloc[0]["Top Duty回数"]), size=12),
                                    Text("Unity Lead回数：" + str(member_data.iloc[0]["Unit Lead回数"]), size=12),
                                    Text("Creative回数：" + str(member_data.iloc[0]["Creative回数"]), size=12),
                                    Text("Help回数：" + str(member_data.iloc[0]["Help回数"]), size=12),
                                ]
                            ),
                        ],
                    ),
                ),
            ],
        )

    def bakan(self):
        print("bakan")