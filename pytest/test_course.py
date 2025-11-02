import pytest
from models.course import Course
from utils.file_handler import FileHandler

@pytest.fixture
def courses_file(tmp_path):
    p = tmp_path / "data" / "courses.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(",".join(Course.FIELDS) + "\n")
    return str(p)

def test_add_new_course_success(courses_file):
    c = Course("DATA200", "Data Foundations", "Intro to data")
    Course.add_new_course(c, file_path=courses_file)
    rows = FileHandler.read_all(courses_file)
    assert len(rows) == 1
    assert rows[0]["course_id"] == "DATA200"
    assert rows[0]["name"] == "Data Foundations"

def test_add_duplicate_course_raises(courses_file):
    c1 = Course("DATA200", "Data Foundations", "Intro to data")
    c2 = Course("DATA200", "Different Name", "Different desc")
    Course.add_new_course(c1, file_path=courses_file)
    with pytest.raises(ValueError, match="Course ID already exists"):
        Course.add_new_course(c2, file_path=courses_file)

def test_update_course_success(courses_file):
    c = Course("DATA200", "Data Foundations", "Intro to data")
    Course.add_new_course(c, file_path=courses_file)
    Course.update_course("DATA200", {"name": "Data Fundamentals"}, file_path=courses_file)
    rows = FileHandler.read_all(courses_file)
    assert rows[0]["name"] == "Data Fundamentals"

def test_update_course_missing_raises(courses_file):
    with pytest.raises(ValueError, match="No course found with id:"):
        Course.update_course("NOPE101", {"name": "X"}, file_path=courses_file)

def test_delete_course_success(courses_file):
    c = Course("DATA200", "Data Foundations", "Intro to data")
    Course.add_new_course(c, file_path=courses_file)
    Course.delete_course("DATA200", file_path=courses_file)
    rows = FileHandler.read_all(courses_file)
    assert rows == []

def test_delete_course_missing_raises(courses_file):
    with pytest.raises(ValueError, match="No course found with id:"):
        Course.delete_course("NOPE101", file_path=courses_file)
