import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def students_above_95():
    above_95 = []

    with open("files/students_structured.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        students = [row for row in reader]

    for student in students:
        marks_dict = eval(student["Marks"])
        total = sum(marks_dict.values())
        percentage = total / 5
        if percentage >= 95:
            above_95.append((student["Name"], percentage))  # ← Use append, not extend

    above_95.sort(key=lambda x: x[1], reverse=True)
    return above_95

def piechart():
    with open("files/students_structured.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        students = [row for row in reader]

    total_students = len(students)
    passed_students = 0
    failed_students = 0
    stud_60to70 = 0
    stud_70to80 = 0
    stud_80to90 = 0
    stud_90to100 = 0

        
    for student in students:
        marks_dict = eval(student["Marks"])
        total = sum(marks_dict.values())
        percentage = total / 5
        if percentage >=60:
            passed_students += 1
        else:
            failed_students += 1

        if percentage >= 60 and percentage < 70:
            stud_60to70 += 1
            
        elif percentage >= 70 and percentage < 80:
            stud_70to80 += 1
        
        elif percentage >= 80 and percentage < 90:
            stud_80to90 += 1
        
        elif percentage >= 90 and percentage <= 100:
            stud_90to100 += 1
            
    # Data for pie chart
    labels = ["<60 %", "60-70 %", "70-80 %", "80-90 %", "90-100 %"]
    sizes = [failed_students, stud_60to70, stud_70to80, stud_80to90, stud_90to100]
    colors = ["red", "orange", "yellow", "green", "blue"]
    explode = (0.1, 0, 0, 0, 0)  # explode the first slice (failed students)
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Student Performance Distribution")
    plt.savefig("files/pie_chart.png")
    print("Pie chart saved as 'files/pie_chart.png'")
    
piechart()

def get_subject_wise_performance(students):
    subject_stats = defaultdict(lambda: {"App": 0, "Pass": 0, "Comp": 0, "Fail": 0})

    for student in students:
        for subject, mark in student["Marks"].items():
            subject_stats[subject]["App"] += 1

            grade = student["Grades"].get(subject, "")
            if grade == "E":
                subject_stats[subject]["Fail"] += 1
            elif student["Result"] == "COMP":
                subject_stats[subject]["Comp"] += 1
            else:
                subject_stats[subject]["Pass"] += 1

    return subject_stats

def get_best_in_subject(students):
    top_scores = defaultdict(lambda: {"Score": -1, "Names": []})

    for student in students:
        for subject, mark in student["Marks"].items():
            if mark > top_scores[subject]["Score"]:
                top_scores[subject]["Score"] = mark
                top_scores[subject]["Names"] = [student["Name"]]
            elif mark == top_scores[subject]["Score"]:
                top_scores[subject]["Names"].append(student["Name"])

    return top_scores

def get_overall_summary(students):
    total = len(students)
    passed = sum(1 for s in students if s["Result"] == "PASS")
    comp = sum(1 for s in students if s["Result"] == "COMP")
    failed = sum(1 for s in students if s["Result"] == "ESSENTIAL REPEAT")
    absent = sum(1 for s in students if s["Result"] == "ABSENT")

    percentages = []
    for s in students:
        total_marks = sum(s["Marks"].values())
        count = len(s["Marks"])
        if count > 0:
            percentages.append(total_marks / count)

    school_avg = round(sum(percentages) / len(percentages), 2) if percentages else 0
    topper = max(percentages) if percentages else 0

    # Band counts
    bands = {
        "90%+": sum(1 for p in percentages if p >= 90),
        "80%+": sum(1 for p in percentages if 80 <= p < 90),
        "70%+": sum(1 for p in percentages if 70 <= p < 80),
        "60%+": sum(1 for p in percentages if 60 <= p < 70),
        "<60%": sum(1 for p in percentages if p < 60),
        "ABST": absent,
    }

    return {
        "Total": total,
        "Passed": passed,
        "Comp": comp,
        "Failed": failed,
        "Topper": round(topper, 2),
        "Average": round(school_avg, 2),
        "Bands": bands,
    }
