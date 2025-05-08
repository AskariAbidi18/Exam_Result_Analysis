import pandas as pd

def generate_excel_report(students, output_path="files/final_output.xlsx"):
    data = []

    for student in students:
        row = [student["Roll No"], student["Name"]]
        subjects = list(student["Marks"].keys())
        total = 0
        count = 0

        for idx in range(6):
            sub = subjects[idx] if idx < len(subjects) else ""
            mark = student["Marks"].get(sub, "") if sub else ""
            grade = student["Grades"].get(sub, "") if sub else ""

            # Add to total and count if mark is valid
            if isinstance(mark, (int, float)):
                total += mark
                count += 1

            row.extend([sub, mark, grade])

        # Compute percentage
        percentage = round(total / count, 2) if count > 0 else 0

        # Append total, percentage, and result
        row.extend([total, percentage, student["Result"]])
        data.append(row)

    # Define column headers
    columns = ["Roll No", "Name"]
    for i in range(1, 7):
        columns += [f"Sub{i}", f"Marks{i}", f"Grade{i}"]
    columns += ["Total", "Percentage", "Result"]

    # Create DataFrame and export to Excel
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(output_path, index=False)
    print(f"Excel report saved to {output_path}")