import re
from typing import List
from backend.core.logger import log_error

from backend.core.models import (
    Student,
    SubjectResult
)

def parse_class12(file_path: str) -> List[Student]:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    students: List[Student] = []

    i = 0

    while i < len(lines):

        line = lines[i].rstrip("\n")

        # detect student line
        if re.match(r"^\d{8}", line):

            # BASIC INFO

            roll_no = line[:8].strip()
            gender = line[8:12].strip()

            # all 3-digit codes
            matches = list(
                re.finditer(r"\b\d{3}\b", line)
            )

            # ignore roll area
            matches = [
                m for m in matches
                if m.start() > 15
            ]

            if not matches:
                i += 1
                continue

            # name
            name = line[
                12:matches[0].start()
            ].strip()

            # subject codes
            subject_codes = [
                m.group()
                for m in matches
            ]

            # remove TOTAL if present
            if len(subject_codes) > 6:
                subject_codes = subject_codes[:-1]

            # RESULT STATUS

            result_match = re.search(
                r"(PASS|COMP|COMPTT|COMPARTMENT|ESSENTIAL REPEAT|ABSENT)",
                line
            )

            result_status = (
                result_match.group(1)
                if result_match
                else "UNKNOWN"
            )

            # MARKS + GRADES

            if i + 1 >= len(lines):
                break

            marks_line = lines[i + 1].strip()

            # pattern:
            # 091 A1 087 B1 etc

            pairs = re.findall(
                r"(\d{2,3})\s+([A-E][1-2]?)",
                marks_line
            )

            marks = []
            grades = []

            for mark, grade in pairs:

                marks.append(int(mark))
                grades.append(grade)

            # validation safety
            min_length = min(
                len(subject_codes),
                len(marks),
                len(grades)
            )

            subject_codes = subject_codes[:min_length]
            marks = marks[:min_length]
            grades = grades[:min_length]
            
            # BUILD SUBJECTS

            subjects: List[SubjectResult] = []

            for code, mark, grade in zip(
                subject_codes,
                marks,
                grades
            ):

                subjects.append(
                    SubjectResult(
                        subject_code=code,
                        subject_name=None,
                        marks=mark,
                        grade=grade
                    )
                )

            # SAVE STUDENT

            students.append(
                Student(
                    roll_no=roll_no,
                    name=name,
                    gender=gender,
                    subjects=subjects,
                    result_status=result_status
                )
            )

            i += 1

        i += 1

    return students
