import pandas as pd
from expense_summary_card import ExpenseSummaryCard
from reward_box import RewardBox
from body import Body
from flet import (
    Column,
    Row,
    Container,
    Text,
    Divider,
    VerticalDivider,
    CrossAxisAlignment,
    Colors,
    ScrollMode
)


class MemberSelectionBody(Body):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        
        # ファイル名, 期間に合致する交通費・交通費意外の経費 のリストを取得
        file_path_list = self.systemLogic.getXlsx(name, "2025-3-1", "2025-12-31")
        transport_expense_list, item_expense_list = self.systemLogic.getExpenseData(file_path_list)

        # 交通費明細ボタン
        self.transport_expense_summary_list: list[ExpenseSummaryCard] = []
        for item in transport_expense_list:
            self.transport_expense_summary_list.append(ExpenseSummaryCard(item[0], item[1], item[2]))

        # 交通費以外の経費明細ボタン
        self.item_expense_summary_list: list[ExpenseSummaryCard] = []
        for item in item_expense_list:
            self.item_expense_summary_list.append(ExpenseSummaryCard(item[0], item[1], item[2]))

        # マスタDBから勤怠実績などのリストを取得
        db = self.systemLogic.getDataset()
        member_row = db.loc[db["名前"] == self.name]

        # NaNであるかを判定して文字列を返す
        def get_val(col_name, is_int=True):
            val = member_row.iloc[0][col_name]
            if pd.isna(val):
                if is_int:
                    return "0"
                else:
                    return "NaN"
            
            if is_int:
                return str(int(val))
            else:
                return str(val)

        # コンテンツ中身
        self.content = Column(
            scroll=ScrollMode.AUTO,
            expand=True,
            spacing=5,
            controls=[
                Text(get_val("名前", is_int=False), size=32),
                Divider(color=Colors.BLACK),
                Text("職位：" + get_val("職位", is_int=False), size=12),
                Text("学籍番号：" + get_val("学籍番号", is_int=True), size=12),
                Container(height=10),
                Container(
                    height=120, # verticalDividerの長さ
                    content=Row(
                        spacing=20,
                        vertical_alignment=CrossAxisAlignment.STRETCH,
                        controls=[
                            Column(
                                controls=[
                                    Text("出席（オンライン含む）：" + get_val("出席（オンライン含む）", is_int=True), size=12),
                                    Text("出張：" + get_val("出張", is_int=True), size=12),
                                    Text("欠席：" + get_val("欠席", is_int=True), size=12),
                                    Text("遅刻：" + get_val("遅刻", is_int=True), size=12),
                                ]
                            ),
                            VerticalDivider(width=1, thickness=1, color=Colors.BLACK),
                            Column(
                                controls=[
                                    Text("現場回数：" + get_val("現場回数", is_int=True), size=12),
                                    Text("Top Duty回数：" + get_val("Top Duty回数", is_int=True), size=12),
                                    Text("Unit Lead回数：" + get_val("Unit Lead回数", is_int=True), size=12),
                                    Text("Creative回数：" + get_val("Creative回数", is_int=True), size=12),
                                    Text("Help回数：" + get_val("Help回数", is_int=True), size=12),
                                ]
                            ),
                        ],
                    ),
                ),
                Container(height=10),
                Text("▼ 交通費申請 一覧 ▼", size=16),
                Row(
                    height=300,
                    vertical_alignment=CrossAxisAlignment.STRETCH,
                    controls=[
                        Container(
                            bgcolor=Colors.GREEN_50,
                            padding=5,
                            expand=True,
                            content = Column(
                                scroll=ScrollMode.AUTO,
                                spacing=5,
                                controls=[
                                    *self.transport_expense_summary_list,
                                ],
                            )
                        ),
                    ]
                ),
                Container(height=10),
                Text("▼ 交通費以外の経費申請 一覧 ▼", size=16),
                Row(
                    height=300,
                    vertical_alignment=CrossAxisAlignment.STRETCH,
                    controls=[
                        Container(
                            bgcolor=Colors.GREEN_50,
                            padding=5,
                            expand=True,
                            content = Column(
                                scroll=ScrollMode.AUTO,
                                spacing=5,
                                controls=[
                                    *self.item_expense_summary_list,
                                ],
                            )
                        ),
                    ]
                ),
                Container(height=10),
                Text("▼ 報酬金記入欄 ▼", size=16),
                RewardBox(),
            ],
        )
