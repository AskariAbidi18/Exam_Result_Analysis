from backend.core.parser import parse_raw_data
from backend.core.analysis import (
    get_toppers,
    get_best_in_subject,
    get_subject_wise_performance
)

students = parse_raw_data("data/raw/raw_data.txt")

print("TOPPERS (>=95):")
for t in get_toppers(students):
    print(t)

print("\nBEST IN SUBJECT:")
best = get_best_in_subject(students)
for k,v in best.items():
    print(k, v)

print("\nSUBJECT PERFORMANCE:")
perf = get_subject_wise_performance(students)
for k,v in perf.items():
    print(k, v)
