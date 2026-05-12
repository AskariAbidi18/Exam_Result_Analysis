import re
from typing import List
from backend.core.models import Student, SubjectResult
from backend.core.constants import SUBJECT_MAP

from backend.core.validators import (
    clean_subject_codes,
    validate_subject_count,
    validate_marks
)

def parse_class10(file_path: str) -> List[Student]:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    students: List[Student] = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip("\n")

        # detect student line
        if re.match(r"^\d{8}", line):

            # -------- BASIC INFO --------
            roll_no = line[:8].strip()
            gender = line[8:12].strip()

            # find subject positions
            matches = list(re.finditer(r"\b\d{3}\b", line))
            matches = [m for m in matches if m.start() > 15]

            if not matches:
                i += 1
                continue

            # name
            name = line[12:matches[0].start()].strip()

            # -------- SUBJECT CODES --------
            nums = [m.group() for m in matches]
            subject_codes = clean_subject_codes(nums)

            if not validate_subject_count(subject_codes):
                print(f"INVALID SUBJECT COUNT -> {roll_no} -> {subject_codes}")
                i += 1
                continue

            # -------- RESULT --------
            result_match = re.search(
                r"(PASS|COMP|COMPTT|COMPARTMENT|ESSENTIAL REPEAT|ABSENT)",
                line
            )
            result_status = result_match.group(1) if result_match else "UNKNOWN"

            # -------- MARKS --------
            if i + 1 >= len(lines):
                break

            marks_line = lines[i + 1].strip()
            marks = list(map(int, re.findall(r"\b\d{2,3}\b", marks_line)))

            # ✅ same structure as subjects
            marks = marks[:len(subject_codes)]

            if not validate_marks(subject_codes, marks):
                print(f"MISMATCH -> {roll_no}")
                i += 1
                continue

            # DEBUG (remove after testing)
            print("DEBUG ->", subject_codes, marks)

            # -------- BUILD SUBJECTS --------
            subjects: List[SubjectResult] = []

            for code, mark in zip(subject_codes, marks):
                subjects.append(
                    SubjectResult(
                        subject_code=code,
                        subject_name=SUBJECT_MAP.get(code),
                        marks=mark,
                        grade="NA"
                    )
                )

            # -------- SAVE STUDENT --------
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