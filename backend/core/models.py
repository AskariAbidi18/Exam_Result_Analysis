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
        return sum(sub.marks for sub in self.subjects)
    
    def percentage(self) -> float:
        if not self.subjects:
            return 0.0
        return round(self.total_marks() / len(self.subjects), 2)
    
@dataclass
class ResultSummary:
    total_students: int
    passed: int
    compartment: int
    failed: int
    topper_percentage: float
    average_percentage: float
    performance_bands: Dict[str, int]