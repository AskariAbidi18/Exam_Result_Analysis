from openpyxl.drawing.image import Image

def write_pie_chart(ws, bands):
    """Insert a pie chart image in the worksheet."""
    img_path = "files/pie_chart.png"
    if not os.path.exists(img_path):
        print("Pie chart image not found at", img_path)
        return
    img = Image(img_path)
    img.anchor = "T35"
    ws.add_image(img)

def write_topper_list(ws, toppers):
    """Write the list of students with >= 95%"""
    ws.append(["STUDENTS WITH 95%"])
    ws.append(["S. No.", "Name of the student", "%AGE"])
    for idx, student in enumerate(toppers, 1):
        ws.append([idx, student["Name"], student["Percentage"]])

def write_subject_performance(ws, subject_stats):
    ws.append(["SUBJECT WISE PERFORMANCE"])
    ws.append(["SUBJECTS", "APP.", "PASS", "COMP.", "FAIL", "PASS%"])
    for subject, stats in subject_stats.items():
        total = stats["App"]
        passed = stats["Pass"]
        percent = round((passed / total) * 100, 2) if total else 0
        ws.append([subject, total, passed, stats["Comp"], stats["Fail"], f"{percent}%"])

def write_best_in_subject(ws, top_scores):
    ws.append(["BEST IN SUBJECT"])
    ws.append(["SUBJECTS", "NAME OF THE STUDENTS", "%AGE"])
    for subject, info in top_scores.items():
        names = ", ".join(info["Names"])
        percentage = round((info["Score"] / 100) * 100, 2)  # Assuming full marks = 100
        ws.append([subject, names, f"{percentage}%"])

def write_overall_summary(ws, summary):
    ws.append(["RESULT AT A GLANCE"])
    ws.append(["", "2023"])
    ws.append(["APPEARED", summary["Total"]])
    ws.append(["PASSED", summary["Passed"]])
    ws.append(["COMPARTMENT", summary["Comp"]])
    ws.append(["FAILED", summary["Failed"]])
    ws.append([])

    ws.append(["COMPARATIVE ANALYSIS OF CLASS XII RESULT 2022-23"])
    ws.append(["Highest", "School Avg.", "90%+", "80%+", "70%+", "60%+", "<60%", "ABST"])
    bands = summary["Bands"]
    ws.append([
        f"{summary['Topper']}%",
        f"{summary['Average']}%",
        bands["90%+"], bands["80%+"], bands["70%+"],
        bands["60%+"], bands["<60%"], bands["ABST"]
    ])