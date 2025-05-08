import csv
import re
import json

def parse_raw_data(input_path):
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    students = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if re.match(r"^\d{8}", line):  # Start of student record
            parts = line.split()
            roll_no = parts[0]
            gender = parts[1]
            name_start_idx = line.find(parts[2])
            name = line[name_start_idx:57].strip()

            # Extract subject codes
            subject_codes = re.findall(r"\d{3}", line[57:])
            result_match = re.search(r"(PASS|COMP|ESSENTIAL REPEAT|ABSENT)", line)
            result = result_match.group(1) if result_match else ""

            # Get next line for marks & grades
            marks_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            marks_values = list(map(int, re.findall(r"\d{2,3}", marks_line)))
            grade_values = re.findall(r"\b[A-D][1-2]|E", marks_line)

            # Build JSON fields
            marks_dict = {subject_codes[idx]: marks_values[idx] for idx in range(min(len(subject_codes), len(marks_values)))}
            grades_dict = {subject_codes[idx]: grade_values[idx] for idx in range(min(len(subject_codes), len(grade_values)))}

            students.append({
                "Roll No": roll_no,
                "Gender": gender,
                "Name": name,
                "Marks": marks_dict,
                "Grades": grades_dict,
                "Result": result
            })

            i += 1  # skip marks line
        i += 1

    return students

def save_students_to_csv(students, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Roll No", "Gender", "Name", "Marks", "Grades", "Result"])
        for student in students:
            writer.writerow([
                student["Roll No"],
                student["Gender"],
                student["Name"],
                json.dumps(student["Marks"]),
                json.dumps(student["Grades"]),
                student["Result"]
            ])

def process_and_save(input_path="files/raw data.txt", output_path="files/students_structured.csv"):
    students = parse_raw_data(input_path)
    save_students_to_csv(students, output_path)
    print(f"Saved structured student data to {output_path}")

process_and_save()
