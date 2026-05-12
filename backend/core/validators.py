from backend.core.constants import MAIN_SUBJECTS

def clean_subject_codes(subject_codes):

    cleaned = []

    for code in subject_codes:

        if code not in MAIN_SUBJECTS:
            continue

        if code not in cleaned:
            cleaned.append(code)

    return cleaned


def validate_subject_count(subject_codes):

    return len(subject_codes) in [5, 6]


def validate_marks(subject_codes, marks):

    return len(subject_codes) == len(marks)
