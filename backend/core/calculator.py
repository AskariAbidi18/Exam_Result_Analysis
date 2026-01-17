from typing import List, Dict
from backend.core.models import Student, ResultSummary


def classify_percentage(percentage: float) -> str:
    if percentage >= 90:
        return "90%+"
    elif percentage >= 80:
        return "80-89%"
    elif percentage >= 70:
        return "70-79%"
    elif percentage >= 60:
        return "60-69%"
    else:
        return "<60%"


def generate_result_summary(students: List[Student]) -> ResultSummary:
    total_students = len(students)
    passed = 0
    compartment = 0
    failed = 0

    percentages: List[float] = []
    performance_bands: Dict[str, int] = {
        "90%+": 0,
        "80-89%": 0,
        "70-79%": 0,
        "60-69%": 0,
        "<60%": 0,
    }

    for student in students:
        percentage = student.percentage()
        percentages.append(percentage)

        # Result status (FIXED)
        if student.result_status == "PASS":
            passed += 1
        elif student.result_status in ("COMP", "COMPTT", "COMPARTMENT"):
            compartment += 1
        else:
            failed += 1

        # Band classification
        band = classify_percentage(percentage)
        performance_bands[band] += 1

    topper_percentage = max(percentages) if percentages else 0.0
    average_percentage = (
        round(sum(percentages) / total_students, 2)
        if total_students else 0.0
    )

    return ResultSummary(
        total_students=total_students,
        passed=passed,
        compartment=compartment,
        failed=failed,
        topper_percentage=topper_percentage,
        average_percentage=average_percentage,
        performance_bands=performance_bands,
    )
