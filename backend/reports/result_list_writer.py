from backend.core.models import Student
from typing import List
from openpyxl.styles import Font, Border, Side, Alignment

bold = Font(bold=True)
thin = Side(style="thin")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center")


def generate_result_sheet(ws, students: List[Student], start_row: int = 2):

    headers = [
        "Roll No", "Name", "Gender",
        "Sub1 Code", "Sub1 Marks",
        "Sub2 Code", "Sub2 Marks",
        "Sub3 Code", "Sub3 Marks",
        "Sub4 Code", "Sub4 Marks",
        "Sub5 Code", "Sub5 Marks",
        "Sub6 Code", "Sub6 Marks",
        "Total Marks", "Percentage", "Result"
    ]

    # HEADERS
    for col, h in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = bold
        cell.border = border
        cell.alignment = center

    ws.freeze_panes = "A2"

    # DATA
    row = start_row

    for student in students:
        col = 1

        ws.cell(row=row, column=col, value=student.roll_no); col += 1
        ws.cell(row=row, column=col, value=student.name); col += 1
        ws.cell(row=row, column=col, value=student.gender); col += 1

        # SUBJECTS
        for subject in student.subjects:
            ws.cell(row=row, column=col, value=subject.subject_code); col += 1
            ws.cell(row=row, column=col, value=subject.marks); col += 1

        # PADDING (FIXED → only 2 cols per subject)
        remaining = 6 - len(student.subjects)
        for _ in range(remaining):
            ws.cell(row=row, column=col, value=""); col += 1
            ws.cell(row=row, column=col, value=""); col += 1

        # TOTAL / %
        ws.cell(row=row, column=col, value=student.total_marks()); col += 1
        ws.cell(row=row, column=col, value=student.percentage()); col += 1
        ws.cell(row=row, column=col, value=student.result_status)

        # BORDERS
        for c in range(1, col + 1):
            ws.cell(row=row, column=c).border = border

        row += 1