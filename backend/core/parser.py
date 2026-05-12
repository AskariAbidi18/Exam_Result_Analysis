from backend.parsers.class10_parser import parse_class10
from backend.parsers.class12_parser import parse_class12


def parse_raw_data(file_path: str, exam_type: str = "10"):

    if exam_type == "10":
        return parse_class10(file_path)

    elif exam_type == "12":
        return parse_class12(file_path)

    else:
        raise ValueError("Invalid exam type")
    