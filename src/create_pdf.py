import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors

class PDFGenerator():
    def __init__(self, filename="output.pdf"):
        self.filename = filename

    def create_pdf(self, data_list=None):
        # 日本語フォントの設定
        font_bold = 'HeiseiKakuGo-W5'
        pdfmetrics.registerFont(UnicodeCIDFont(font_bold))

        # 保存先を指定してキャンバスを作成
        # 原点は左下
        pdf_canvas = canvas.Canvas(self.filename, pagesize=portrait(A4))
        A4_HEIGHT = 297 * mm
        A4_WIDTH = 210 * mm
        
        # 日付
        pdf_canvas.setFont(font_bold, 10)
        pdf_canvas.drawRightString(A4_WIDTH - 15 * mm, A4_HEIGHT - 15 * mm, "発行日：yyyy-MM-dd")

        # ヘッダー
        pdf_canvas.setFont(font_bold, 24)
        pdf_canvas.drawCentredString(A4_WIDTH/2, A4_HEIGHT - 30 * mm, "活動費支給明細書")

        # 基本情報
        pdf_canvas.setFont(font_bold, 10)
        pdf_canvas.drawString(15 * mm, A4_HEIGHT - 45 * mm, "名前：こんにちは")
        pdf_canvas.drawString(15 * mm, A4_HEIGHT - 52 * mm, "職位：こんにちは")
        pdf_canvas.drawString(15 * mm, A4_HEIGHT - 59 * mm, "学籍番号：37298753")

        # 勤怠実績
        attend_data = [
            ["出席日数(オンライン含む)", "xx"],
            ["欠席日数", "xx"],
            ["出張日数", "xx"],
            ["早退日数", "xx"],
            ["", ""]
        ]
        attend_table = Table(attend_data, colWidths=(60 * mm, 25 * mm), rowHeights=(7 * mm))
        attend_table.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), font_bold, 10),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        attend_table.wrapOn(pdf_canvas, 15 * mm, A4_HEIGHT - 100 * mm)
        attend_table.drawOn(pdf_canvas, 15 * mm, A4_HEIGHT - 100 * mm)

        # 勤怠実績2
        role_data = [
            ["現場回数", "xx"],
            ["Top Duty回数", "xx"],
            ["Unit Lead回数", "xx"],
            ["Creative回数", "xx"],
            ["Help回数", "xx"]
        ]
        role_table = Table(role_data, colWidths=(60 * mm, 25 * mm), rowHeights=(7 * mm))
        role_table.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), font_bold, 10),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        role_table.wrapOn(pdf_canvas, A4_WIDTH/2 + 5 * mm, A4_HEIGHT - 100 * mm)
        role_table.drawOn(pdf_canvas, A4_WIDTH/2 + 5 * mm, A4_HEIGHT - 100 * mm)

        # 支給明細
        column_name = [
            ["報酬金支給", "交通費/立替金支給", "天引き金額"]
        ]
        column_table = Table(column_name, colWidths=((A4_WIDTH - 30 * mm)/3), rowHeights=(7 * mm))
        column_table.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), font_bold, 10),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        column_table.wrapOn(pdf_canvas, 15 * mm, A4_HEIGHT - 110 * mm)
        column_table.drawOn(pdf_canvas, 15 * mm, A4_HEIGHT - 110 * mm)

        # 支給明細
        payment_data = [["摘要", "金額", "摘要", "金額", "摘要", "金額"]]
        rows = [["こんにちは", i + 10000, "こんにちは", i, "こんにちは", i] for i in range(0, 20)]
        payment_data.extend(rows) # または payment_data += rows
        payment_table = Table(
            payment_data, 
            colWidths=(
                ((A4_WIDTH - 30 * mm)/3)/3 * 2,
                ((A4_WIDTH - 30 * mm)/3)/3,
                ((A4_WIDTH - 30 * mm)/3)/3 * 2,
                ((A4_WIDTH - 30 * mm)/3)/3,
                ((A4_WIDTH - 30 * mm)/3)/3 * 2,
                ((A4_WIDTH - 30 * mm)/3)/3,
                ), 
            rowHeights=(7 * mm)
        )
        payment_table.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), font_bold, 8),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
            # ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        payment_table.wrapOn(pdf_canvas, 15 * mm, 40 * mm)
        payment_table.drawOn(pdf_canvas, 15 * mm, 40 * mm)

        # 合計金額
        total_data = [
            ["合計", "XX,XXX" + " 円"]
        ]
        total_table = Table(total_data, colWidths=((A4_WIDTH - 30 * mm)/4), rowHeights=(7 * mm))
        total_table.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), font_bold, 10),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        total_table.wrapOn(pdf_canvas, A4_WIDTH/2, 15 * mm)
        total_table.drawOn(pdf_canvas, A4_WIDTH/2, 15 * mm)

        # 押印欄
        column_name = [
            ["支給金確定者", "実績確定者"],
            ["印", "印"]
        ]
        column_table = Table(column_name, colWidths=(18 * mm), rowHeights=(5 * mm, 18 * mm))
        column_table.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, -1), font_bold, 5),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        column_table.wrapOn(pdf_canvas, 15 * mm, 10 * mm)
        column_table.drawOn(pdf_canvas, 15 * mm, 10 * mm)




        # # --- 社名部分（Table） ---
        # company_data = [
        #     ["ほげほげ会社御中", ""],
        #     ["案件名", "ほげほげ案件"],
        #     ["御見積有効限：発行日より30日", ""],
        # ]
        # table = Table(company_data, colWidths=(40 * mm, 80 * mm), rowHeights=(7 * mm))
        # table.setStyle(TableStyle([
        #     ("FONT", (0, 0), (-1, -1), font_bold, 12),
        #     ("LINEBELOW", (0, 0), (0, 1), 1, colors.black), # 下線
        #     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        # ]))
        # table.wrapOn(pdf_canvas, 20 * mm, 240 * mm)
        # table.drawOn(pdf_canvas, 20 * mm, 240 * mm)

        # pdf_canvas.drawString(20 * mm, 230 * mm, "下記の通り御見積申し上げます")

        # # --- 合計金額 ---
        # total_data = [["合計金額（消費税込）", "1,100 円"]]
        # total_table = Table(total_data, colWidths=(50 * mm, 40 * mm), rowHeights=(10 * mm))
        # total_table.setStyle(TableStyle([
        #     ("FONT", (0, 0), (-1, -1), font_bold, 12),
        #     ("BOX", (0, 0), (-1, -1), 1, colors.black),
        #     ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
        #     ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        #     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        # ]))
        # total_table.wrapOn(pdf_canvas, 20 * mm, 210 * mm)
        # total_table.drawOn(pdf_canvas, 20 * mm, 210 * mm)

        # # --- 品目明細 ---
        # items_data = [["内容", "開始月", "終了月", "単価", "数量", "金額"]]
        # for _ in range(10):  # 空行
        #     items_data.append([" ", " ", " ", " ", " ", " "])
        
        # items_data.append(["", "", "", "合計", "", "1,000"])
        # items_data.append(["", "", "", "消費税", "", "100"])
        # items_data.append(["", "", "", "税込合計", "", "1,100"])

        # item_table = Table(items_data, colWidths=(60 * mm, 25 * mm, 25 * mm, 20 * mm, 20 * mm, 25 * mm), rowHeights=7 * mm)
        # item_table.setStyle(TableStyle([
        #     ("FONT", (0, 0), (-1, -1), font_bold, 9),
        #     ("BOX", (0, 0), (-1, 10), 1, colors.black),
        #     ("INNERGRID", (0, 0), (-1, 10), 1, colors.black),
        #     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        #     ("ALIGN", (3, 0), (-1, -1), "RIGHT"),
        # ]))
        # item_table.wrapOn(pdf_canvas, 17 * mm, 120 * mm)
        # item_table.drawOn(pdf_canvas, 17 * mm, 120 * mm)

        # # --- 備考欄 ---
        # pdf_canvas.drawString(17 * mm, 110 * mm, "<備考>")
        # memo_table = Table([[""]], colWidths=(180 * mm), rowHeights=50 * mm)
        # memo_table.setStyle(TableStyle([
        #     ("BOX", (0, 0), (-1, -1), 1, colors.black),
        # ]))
        # memo_table.wrapOn(pdf_canvas, 17 * mm, 55 * mm)
        # memo_table.drawOn(pdf_canvas, 17 * mm, 55 * mm)

        # 保存
        pdf_canvas.showPage()
        pdf_canvas.save()
        print(f"PDF作成完了: {os.path.abspath(self.filename)}")

# 実行テスト
if __name__ == "__main__":
    gen = PDFGenerator("/Users/daiki/Desktop/shadecor-finance-analyzer/pdf_folder/test.pdf")
    gen.create_pdf()