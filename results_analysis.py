import csv
import matplotlib.pyplot as plt
from collections import defaultdict

def students_above_95():
    import ast  # Safer alternative to eval
    above_95 = []

    with open("files/students_structured.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        students = [row for row in reader]

    for student in students:
        try:
            marks_dict = ast.literal_eval(student["Marks"])  # Safely parse stored string
            if not marks_dict:
                continue
            total = sum(marks_dict.values())
            percentage = total / len(marks_dict)
            if percentage >= 95:
                above_95.append((student["Name"], percentage))
        except Exception as e:
            print(f"Skipping student due to error: {e}")
            continue

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

def get_subject_wise_average_from_csv(csv_path="files/students_structured.csv"):
    subject_totals = defaultdict(int)
    subject_counts = defaultdict(int)

    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            marks = eval(row["Marks"])  # Convert string to dictionary
            for subject_code, score in marks.items():
                subject_totals[subject_code] += score
                subject_counts[subject_code] += 1

    subject_averages = {
        subject: round(subject_totals[subject] / subject_counts[subject], 2)
        for subject in subject_totals
    }

    return subject_averages