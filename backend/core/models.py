from dataclasses import dataclass, field
from typing import List, Dict 

@dataclass
class SubjectResult:
    subject_code : str
    subject_name : str | None
    marks : int
    grade : str

@dataclass 
class Student:
    roll_no : str
    name : str
    gender : str
    subjects : List[SubjectResult] = field(default_factory=list)
    result_status : str = "PASS"

    def total_marks(self) -> int:
        marks = [sub.marks for sub in self.subjects]
        return sum(sorted(marks, reverse=True)[:5])
    
    def percentage(self) -> float:
        if not self.subjects:
            return 0.0

        marks = [sub.marks for sub in self.subjects]

        # BEST 5 ONLY
        best_five = sorted(marks, reverse=True)[:5]

        return round(sum(best_five) / 5, 2)
    
@dataclass
class ResultSummary:
    total_students: int
    passed: int
    compartment: int
    failed: int
    topper_percentage: float
    average_percentage: float
    performance_bands: Dict[str, int]