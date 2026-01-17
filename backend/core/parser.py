import re
from typing import List
from backend.core.models import Student, SubjectResult


def parse_raw_data(file_path: str) -> List[Student]:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    students: List[Student] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip("\n")

        # Start of a student record
        if re.match(r"^\d{8}", line):

            parts = line.split()
            roll_no = parts[0]
            gender = parts[1]

            # Extract name (fixed CBSE width format)
            name_start = line.find(parts[2])
            name = line[name_start:57].strip()

            # Subject codes
            subject_codes = re.findall(r"\d{3}", line[57:])

            # Result status (expanded regex)
            result_match = re.search(
                r"(PASS|COMP|COMPTT|COMPARTMENT|ESSENTIAL REPEAT|ABSENT)",
                line
            )
            result_status = result_match.group(1) if result_match else "UNKNOWN"

            # Next line = marks + grades
            marks_line = lines[i + 1].strip()

            marks = list(map(int, re.findall(r"\d{2,3}", marks_line)))
            grades = re.findall(r"\b[A-D][1-2]|E\b", marks_line)

            subjects: List[SubjectResult] = []

            for idx in range(min(len(subject_codes), len(marks), len(grades))):
                subjects.append(
                    SubjectResult(
                        subject_code=subject_codes[idx],
                        subject_name=None,
                        marks=marks[idx],
                        grade=grades[idx],
                    )
                )

            students.append(
                Student(
                    roll_no=roll_no,
                    name=name,
                    gender=gender,
                    subjects=subjects,
                    result_status=result_status,
                )
            )

            i += 1  # skip marks line

        i += 1

    return students
