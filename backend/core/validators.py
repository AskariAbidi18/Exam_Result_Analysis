from backend.core.constants import MAIN_SUBJECTS

def clean_subject_codes(subject_codes):

    cleaned = []

    for code in subject_codes:

        if code not in MAIN_SUBJECTS:
            continue

        if code not in cleaned:
            cleaned.append(code)

    return cleaned
