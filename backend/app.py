from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uuid
import os

from openpyxl import load_workbook

from backend.core.parser import parse_raw_data
from backend.core.calculator import generate_result_summary
from backend.core.analysis import (
    get_toppers,
    get_best_in_subject,
    get_subject_wise_performance
)
from backend.reports.excel_writer import generate_analysis_sheet
from backend.reports.result_list_writer import generate_result_sheet

app = FastAPI()

RAW_DIR = "data/raw"
OUTPUT_DIR = "data/output"

CBSE_TEMPLATE = "data/output/test_result_sheet.xlsx"
ANALYSIS_TEMPLATE = "backend/reports/templates/Result Analysis 2023 Class XII.xlsx"


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    raw_path = f"{RAW_DIR}/{uuid.uuid4()}.txt"

    with open(raw_path, "wb") as f:
        f.write(await file.read())

    output_file = generate_report(raw_path)

    return FileResponse(
        output_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="Final_CBSE_Result.xlsx"
    )


def generate_report(raw_path):

    # Load CBSE formatted workbook
    wb = load_workbook(CBSE_TEMPLATE)

    # -------- RESULT SHEET (Sheet 7) --------
    result_ws = wb.worksheets[6]
    students = parse_raw_data(raw_path)
    generate_result_sheet(result_ws, students)

    # -------- ANALYSIS SHEET (Sheet 2) --------
    template_wb = load_workbook(ANALYSIS_TEMPLATE)
    template_ws = template_wb.active

    analysis_ws = wb.copy_worksheet(template_ws)
    analysis_ws.title = "Analysis"

    # Move to 2nd position
    wb._sheets.remove(analysis_ws)
    wb._sheets.insert(1, analysis_ws)

    # Compute stats
    summary = generate_result_summary(students)
    toppers = get_toppers(students)
    best_subjects = get_best_in_subject(students)
    subject_perf = get_subject_wise_performance(students)

    # Fill analysis
    generate_analysis_sheet(
        analysis_ws,
        summary,
        toppers,
        best_subjects,
        subject_perf
    )

    # Save new file
    out_file = f"{OUTPUT_DIR}/final_{uuid.uuid4()}.xlsx"
    wb.save(out_file)

    return out_file
