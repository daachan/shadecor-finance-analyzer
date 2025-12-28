from layout import MyLayout
from flet import (
    app,
    Page,
    Row
)

def main(page: Page):
    page.title = "活動費明細書ジェネレータ"
    page.padding = 0

    page.add(MyLayout(page))

if __name__ == '__main__':
    app(target=main)
