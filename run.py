from initial_data_processor import parse_raw_data, save_students_to_csv
from excel_report_generator import generate_excel_report
from results_analysis import students_above_95, piechart
from analysis_excel import write_above_95_to_excel
import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

RAW_INPUT_PATH = "files/raw data.txt"
CSV_OUTPUT_PATH = "files/students_structured.csv"
EXCEL_OUTPUT_PATH = "files/Boards Results.xlsx"
RESULT_ANALYSIS_PATH = "files/result_analysis.xlsx"
PIECHART_PATH = "files/pie_chart.png"  # Path to the saved pie chart image

def main():
    # Step 1: Parse the raw text file
    students = parse_raw_data(RAW_INPUT_PATH)

    # Step 2: Save structured student data to CSV (optional for inspection)
    save_students_to_csv(students, CSV_OUTPUT_PATH)

    # Step 3: Generate the final formatted Excel sheet
    generate_excel_report(students, EXCEL_OUTPUT_PATH)
    
    # Step 4: Get students above 95%
    top_students = students_above_95()
    
    # Step 5: Write analysis data to Excel
    write_above_95_to_excel(RESULT_ANALYSIS_PATH)
    
    # Step 6: Generate the pie chart (should save to PIECHART_PATH)
    piechart()  # Ensure this function saves the chart to PIECHART_PATH

    # Step 7: Read both Excel files
    result_file = pd.read_excel(EXCEL_OUTPUT_PATH)
    analysis_file = pd.read_excel(RESULT_ANALYSIS_PATH)

    # Step 8: Create a combined Excel file with both sheets
    combined_path = 'files/integrated_report.xlsx'
    with pd.ExcelWriter(combined_path) as writer:
        result_file.to_excel(writer, sheet_name='Result', index=False)
        analysis_file.to_excel(writer, sheet_name='Analysis', index=False)

    # Step 9: Insert the pie chart image into the 'Analysis' sheet
    wb = load_workbook(combined_path)
    sheet = wb['Analysis']

    img = Image(PIECHART_PATH)
    img.width = 350   # Resize the image width (in pixels)
    img.height = 350  # Resize the image height (in pixels)

    sheet.add_image(img, 'D2')  # Adjust the cell location as needed

    wb.save(combined_path)

    print("The integrated Excel file 'integrated_report.xlsx' has been created with two sheets and a resized pie chart.")

if __name__ == "__main__":
    main()
    print("Processing Complete, file saved to files/integrated_report.xlsx")
