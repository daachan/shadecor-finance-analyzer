from box import Box
from reward_registered_card import RewardRegisteredCard
import datetime
from flet import (
    Container,
    Colors,
    Column,
    ScrollMode,
    IconButton,
    Icons,
    CrossAxisAlignment
)

class RewardBox(Box):
    def __init__(self):
        super().__init__()

        # 報酬金の登録リスト
        self.reward_register_list: list[RewardRegisteredCard] = []

        def delete_reward_card(serial_num):
            for item in self.reward_register_list:
                if item.serial_num == serial_num:
                    print("delete:" + item.serial_num)
                    self.reward_register_list.remove(item)
                    break
            
            self.controls=[
                Container(
                    bgcolor=self.box_color,
                    padding=self.box_padding,
                    expand=True,
                    content = Column(
                        scroll=ScrollMode.AUTO,
                        spacing=5,
                        controls=[
                            *self.reward_register_list,
                            IconButton(icon=Icons.ADD, on_click=add_reward_card, expand=True)
                        ],
                    )
                ),
            ]
            self.page.update()
                    

        def add_reward_card():
            serial = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            print("serial_num:" + serial)
            self.reward_register_list.append(RewardRegisteredCard(serial_num=serial, func_delete=delete_reward_card))

            self.controls=[
                Container(
                    bgcolor=self.box_color,
                    padding=self.box_padding,
                    expand=True,
                    content = Column(
                        scroll=ScrollMode.AUTO,
                        spacing=5,
                        controls=[
                            *self.reward_register_list,
                            IconButton(icon=Icons.ADD, on_click=add_reward_card, expand=True)
                        ],
                    )
                ),
            ]
            self.page.update()

        self.controls=[
            Container(
                bgcolor=self.box_color,
                padding=self.box_padding,
                expand=True,
                content = Column(
                    scroll=ScrollMode.AUTO,
                    spacing=5,
                    controls=[
                        *self.reward_register_list,
                        IconButton(icon=Icons.ADD, on_click=add_reward_card, bgcolor=Colors.WHITE, expand=True)
                    ],
                )
            ),
        ]

    
