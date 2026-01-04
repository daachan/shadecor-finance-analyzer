import os
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors

from drivePresenter import GoogleDrivePresenter
from member_selection_body import MemberSelectionBody

class PDFGenerator():
    def __init__(self, name="no_arg_output", body_list: list[MemberSelectionBody] = []):
        # Bodyの設定情報を取得
        self.pick_body : MemberSelectionBody
        for body in body_list:
            if body.name == name:
                self.pick_body = body
                break
        # 交通費
        self.expense_summary_dict : dict[str, int] = {}
        self.expense_total : int = 0 #ついでに合計も計算
        for item in self.pick_body.transport_expense_summary_list:
            if item.checkFrag:
                fn = str(item.file_name)
                parts = fn.split("_")
                info = f"【交通費】申請日：{parts[1]}_{parts[2]}"
                
                self.expense_total += item.value

                if info in self.expense_summary_dict:
                    self.expense_summary_dict[info] += item.value
                else:
                    self.expense_summary_dict[info] = item.value
        # 交通費以外の経費
        for item in self.pick_body.item_expense_summary_list:
            if item.checkFrag:
                fn = str(item.file_name)
                parts = fn.split("_")
                info = f"【その他】申請日：{parts[1]}_{parts[2]}"

                self.expense_total += item.value

                if info in self.expense_summary_dict:
                    self.expense_summary_dict[info] += item.value
                else:
                    self.expense_summary_dict[info] = item.value

        # 明細データの正規化
        self.ROW_NUM = 20 #現在の出力行数
        def fix_dict_to_list(summary_dict: dict[str, int], num: int):
            item_list = [[text, cost] for text, cost in summary_dict.items()]
            padding_size = 20 - len(item_list)
            output_list = (item_list + [["", ""]] * padding_size)[:20]
            return output_list
        
        self.expense_summary = fix_dict_to_list(self.expense_summary_dict, 20)

        # 日時
        now = datetime.now()
        self.date = now.strftime("%Y-%m-%d")
        
        # 保存時のファイルパス
        self.username = name
        self.filepath = "/Users/daiki/Desktop/shadecor-finance-analyzer/pdf_folder/" + name + "_" + self.date + ".pdf"
        
        # 勤怠情報の読み込み
        self.systemLogic = GoogleDrivePresenter()
        db = self.systemLogic.getDataset()
        user_data = db[db["名前"] == self.username]

        # NaNであるかを判定して文字列を返す
        def get_val(col_name, is_int=True):
            val = user_data.iloc[0][col_name]
            if pd.isna(val):
                if is_int:
                    return "0"
                else:
                    return "NaN"

            if is_int:
                return str(int(val))
            else:
                return str(val)

        self.student_id = get_val("学籍番号", is_int=True)
        self.role = get_val("職位", is_int=False)
        self.attend_num = get_val("出席（オンライン含む）", is_int=True)
        self.absent_num = get_val("欠席", is_int=True)
        self.trip_num = get_val("出張", is_int=True)
        self.late_num = get_val("遅刻", is_int=True)
        self.onsite_num = get_val("現場回数", is_int=True)
        self.top_duty_num = get_val("Top Duty回数", is_int=True)
        self.unit_lead_num = get_val("Unit Lead回数", is_int=True)
        self.creative_num = get_val("Creative回数", is_int=True)
        self.help_num = get_val("Help回数", is_int=True)

    def create_pdf(self, data_list=None):
        # 日本語フォントの設定
        font_bold = 'HeiseiKakuGo-W5'
        pdfmetrics.registerFont(UnicodeCIDFont(font_bold))

        # 保存先を指定してキャンバスを作成
        # 原点は左下
        pdf_canvas = canvas.Canvas(self.filepath, pagesize=portrait(A4))
        A4_HEIGHT = 297 * mm
        A4_WIDTH = 210 * mm
        
        # 日付
        pdf_canvas.setFont(font_bold, 10)
        pdf_canvas.drawRightString(A4_WIDTH - 15 * mm, A4_HEIGHT - 15 * mm, "発行日：" + self.date)

        # ヘッダー
        pdf_canvas.setFont(font_bold, 24)
        pdf_canvas.drawCentredString(A4_WIDTH/2, A4_HEIGHT - 30 * mm, "活動費支給明細書")

        # 基本情報
        pdf_canvas.setFont(font_bold, 10)
        pdf_canvas.drawString(15 * mm, A4_HEIGHT - 45 * mm, "名前：" + self.username)
        pdf_canvas.drawString(15 * mm, A4_HEIGHT - 52 * mm, "職位：" + self.role)
        pdf_canvas.drawString(15 * mm, A4_HEIGHT - 59 * mm, "学籍番号：" + self.student_id)

        # 勤怠実績
        attend_data = [
            ["出席日数(オンライン含む)", self.attend_num],
            ["欠席日数", self.absent_num],
            ["出張日数", self.trip_num],
            ["遅刻日数", self.late_num],
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
            ["現場回数", self.onsite_num],
            ["Top Duty回数", self.top_duty_num],
            ["Unit Lead回数", self.unit_lead_num],
            ["Creative回数", self.creative_num],
            ["Help回数", self.help_num]
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
        rows = [["こんにちは", i + 10000, self.expense_summary[i][0], self.expense_summary[i][1], "こんにちは", i] for i in range(0, 20)]
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
            ("FONT", (0, 0), (-1, -1), font_bold, 5),
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
            ("FONT", (0, 0), (-1, -1), font_bold, 6),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        column_table.wrapOn(pdf_canvas, 15 * mm, 10 * mm)
        column_table.drawOn(pdf_canvas, 15 * mm, 10 * mm)

        # 保存
        pdf_canvas.showPage()
        pdf_canvas.save()
        print(f"PDF作成完了: {os.path.abspath(self.filepath)}")