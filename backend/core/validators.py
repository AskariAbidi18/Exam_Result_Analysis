from backend.core.constants import MAIN_SUBJECTS
from backend.core.logger import log_error


def clean_subject_codes(subject_codes):

    cleaned = []

    for code in subject_codes:

        if code not in MAIN_SUBJECTS:
            continue

        if code not in cleaned:
            cleaned.append(code)

    return cleaned


def validate_subject_count(subject_codes, roll_no):

    valid = len(subject_codes) in [5, 6]

    if not valid:

        log_error(
            f"INVALID SUBJECT COUNT -> "
            f"{roll_no} -> {subject_codes}"
        )

    return valid


def validate_marks(subject_codes, marks, roll_no):

    valid = len(subject_codes) == len(marks)

    if not valid:

        log_error(
            f"MARKS MISMATCH -> "
            f"{roll_no} -> "
            f"Subjects={subject_codes} "
            f"Marks={marks}"
        )

    return valid
    