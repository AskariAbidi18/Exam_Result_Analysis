from initial_data_processor import parse_raw_data, save_students_to_csv, process_and_save
from excel_report_generator import generate_excel_report
from results_analysis import students_above_95, get_best_in_subject, get_subject_wise_average_from_csv
import pandas as pd
from openpyxl import load_workbook

RAW_INPUT_PATH = "files/raw data.txt"
CSV_OUTPUT_PATH = "files/students_structured.csv"
EXCEL_OUTPUT_PATH = "files/Boards Results.xlsx"
RESULT_ANALYSIS_PATH = "files/result_analysis.xlsx"
COMBINED_REPORT_PATH = "files/integrated_report.xlsx"

def main():
    # Step 1: Parse and process student data
    students = parse_raw_data(RAW_INPUT_PATH)
    process_and_save()
    save_students_to_csv(students, CSV_OUTPUT_PATH)
    generate_excel_report(students, EXCEL_OUTPUT_PATH)

    # Step 2: Run analysis
    top_students = students_above_95()
    best_subjects = get_best_in_subject(students)

    # Step 3: Prepare DataFrames
    df_top = pd.DataFrame(top_students, columns=["Name", "Percentage"])
    
    df_best_subjects = pd.DataFrame([
        {
            "Subject": subject,
            "Top Score": data["Score"],
            "Topper(s)": ", ".join(data["Names"])
        }
        for subject, data in best_subjects.items()
    ])

    # Step 4: Get subject-wise averages
    subject_averages = get_subject_wise_average_from_csv(CSV_OUTPUT_PATH)
    df_subject_avg = pd.DataFrame([
        {"Subject Code": code, "Average Marks": avg}
        for code, avg in subject_averages.items()
    ])

    # Step 5: Save to result_analysis.xlsx (optional)
    with pd.ExcelWriter(RESULT_ANALYSIS_PATH) as writer:
        df_top.to_excel(writer, sheet_name="Above 95%", index=False)
        df_best_subjects.to_excel(writer, sheet_name="Best in Subject", index=False)
        df_subject_avg.to_excel(writer, sheet_name="Subject-wise Averages", index=False)

    # Step 6: Create integrated_report.xlsx with 'Result' + 'Analysis'
    with pd.ExcelWriter(COMBINED_REPORT_PATH, engine='openpyxl') as writer:
        # Write the result sheet
        pd.read_excel(EXCEL_OUTPUT_PATH).to_excel(writer, sheet_name='Result', index=False)
        
        # Write the analysis section
        df_top.to_excel(writer, sheet_name='Analysis', index=False, startrow=0)
        df_best_subjects.to_excel(writer, sheet_name='Analysis', index=False, startrow=len(df_top) + 3)
        df_subject_avg.to_excel(writer, sheet_name='Analysis', index=False, startrow=len(df_top) + len(df_best_subjects) + 6)

    print("✅ Integrated report generated at:", COMBINED_REPORT_PATH)

if __name__ == "__main__":
    main()
    print("Processing Complete.")
