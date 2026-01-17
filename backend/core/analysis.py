from typing import List, Dict
from collections import defaultdict
from backend.core.models import Student


def get_toppers(students: List[Student], threshold: float = 95.0) -> List[dict]:
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

    toppers.sort(key=lambda x: x["percentage"], reverse=True)
    return toppers


def get_best_in_subject(students: List[Student]) -> Dict[str, dict]:
    """
    Returns best performer(s) per subject based on MARKS
    """
    subject_best = {}

    for student in students:
        for subject in student.subjects:
            percentage = subject.marks

            if subject.subject_code not in subject_best:
                subject_best[subject.subject_code] = {
                    "percentage": percentage,
                    "students": [student.name]
                }
            else:
                if percentage > subject_best[subject.subject_code]["percentage"]:
                    subject_best[subject.subject_code] = {
                        "percentage": percentage,
                        "students": [student.name]
                    }
                elif percentage == subject_best[subject.subject_code]["percentage"]:
                    subject_best[subject.subject_code]["students"].append(student.name)

    return subject_best


def get_subject_wise_performance(students: List[Student]) -> Dict[str, dict]:
    """
    Computes appeared, pass, fail and pass percentage per subject
    """
    stats = defaultdict(lambda: {
        "appeared": 0,
        "pass": 0,
        "fail": 0
    })

    for student in students:
        for subject in student.subjects:
            code = subject.subject_code
            stats[code]["appeared"] += 1

            if subject.grade == "E":
                stats[code]["fail"] += 1
            else:
                stats[code]["pass"] += 1

    for code, data in stats.items():
        appeared = data["appeared"]
        passed = data["pass"]
        data["pass_percentage"] = round(
            (passed / appeared) * 100, 2
        ) if appeared else 0.0

    return dict(stats)
