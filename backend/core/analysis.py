from typing import List, Dict
from collections import defaultdict

from backend.core.models import Student
from backend.core.constants import SUBJECT_MAP

def get_toppers(
    students: List[Student],
    threshold: float = 95.0
) -> List[dict]:
    """
    Returns students with percentage >= threshold
    """

    toppers = []

    for student in students:

        percentage = student.percentage()

        if percentage >= threshold:

            toppers.append({
                "name": student.name,
                "percentage": percentage
            })

    toppers.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return toppers

def get_best_in_subject(
    students: List[Student]
) -> Dict[str, dict]:
    """
    Returns best performer(s) per subject
    based on highest marks
    """

    subject_best = {}

    for student in students:

        for subject in student.subjects:

            subject_name = SUBJECT_MAP.get(
                subject.subject_code,
                subject.subject_code
            )

            marks = subject.marks

            if subject_name not in subject_best:

                subject_best[subject_name] = {
                    "marks": marks,
                    "students": [student.name]
                }

            else:

                current_best = subject_best[subject_name]["marks"]

                if marks > current_best:

                    subject_best[subject_name] = {
                        "marks": marks,
                        "students": [student.name]
                    }

                elif marks == current_best:

                    subject_best[subject_name]["students"].append(
                        student.name
                    )

    return subject_best

def get_subject_wise_performance(
    students: List[Student]
) -> Dict[str, dict]:
    """
    Computes:
    - appeared
    - pass
    - fail
    - pass percentage

    SUBJECT-CENTRIC
    """

    stats = defaultdict(lambda: {
        "appeared": 0,
        "pass": 0,
        "fail": 0
    })

    for student in students:

        for subject in student.subjects:

            subject_name = SUBJECT_MAP.get(
                subject.subject_code,
                subject.subject_code
            )

            stats[subject_name]["appeared"] += 1

            # CBSE passing marks logic
            if subject.marks < 33:

                stats[subject_name]["fail"] += 1

            else:

                stats[subject_name]["pass"] += 1

    # Calculate pass percentage
    for subject_name, data in stats.items():

        appeared = data["appeared"]
        passed = data["pass"]

        data["pass_percentage"] = round(
            (passed / appeared) * 100,
            2
        ) if appeared else 0.0

    return dict(stats)
