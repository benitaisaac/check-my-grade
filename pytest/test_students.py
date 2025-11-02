import os
import pytest
from models.student import Student
from utils.file_handler import FileHandler

@pytest.fixture
def students_file(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data_dir / "students.csv"
    # seed header
    with open(csv_path, "w") as f:
        f.write(",".join(Student.FIELDS) + "\n")
    return str(csv_path)

def test_add_new_student_success(students_file):
    s = Student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", "A", 96)
    Student.add_new_student(s, file_path=students_file)
    rows = FileHandler.read_all(students_file)
    assert len(rows) == 1
    assert rows[0]["email"] == "sam@mycsu.edu"

def test_add_duplicate_student_raises(students_file):
    s1 = Student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", "A", 96)
    s2 = Student("sam@mycsu.edu", "Samuel", "Cooper", "DATA210", "B", 88)
    Student.add_new_student(s1, file_path=students_file)
    with pytest.raises(ValueError, match="Email already exists"):
        Student.add_new_student(s2, file_path=students_file)

def test_delete_student_success(students_file):
    s = Student("lily@mycsu.edu", "Lily", "Nguyen", "DATA210", "B", 88)
    Student.add_new_student(s, file_path=students_file)
    Student.delete_student("lily@mycsu.edu", file_path=students_file)
    rows = FileHandler.read_all(students_file)
    assert rows == []

def test_delete_student_missing_raises(students_file):
    with pytest.raises(ValueError, match="No student found with email:"):
        Student.delete_student("ghost@mycsu.edu", file_path=students_file)

def test_update_student_success(students_file):
    s = Student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", "A", 96)
    Student.add_new_student(s, file_path=students_file)
    Student.update_student("sam@mycsu.edu", {"grade": "B", "marks": 85}, file_path=students_file)
    rows = FileHandler.read_all(students_file)
    assert rows[0]["grade"] == "B"
    assert int(rows[0]["marks"]) == 85

def test_update_student_missing_raises(students_file):
    with pytest.raises(ValueError, match="No student found with email:"):
        Student.update_student("ghost@mycsu.edu", {"grade": "A"}, file_path=students_file)
