# models/student.py
import time
from statistics import median
from utils.file_handler import FileHandler

class Student:
    DATA_FILE = "data/students.csv"
    FIELDS = ["email", "first_name", "last_name", "course_id", "grade", "marks"]

    def __init__(self, email, first_name, last_name, course_id, grade, marks):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grade = grade
        self.marks = int(marks) if str(marks).isdigit() else marks

    def display_records(self):
        print(f"{self.first_name} {self.last_name} - {self.course_id} - {self.grade} ({self.marks})")


    # CRUD METHODS
    @staticmethod
    def add_new_student(student, file_path: str = None):
        file_path = file_path or Student.DATA_FILE
        students = FileHandler.read_all(file_path)

        for row in students:
            if row.get("email") == student.email:
                raise ValueError("Email already exists")

        row = {
            "email": student.email,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "course_id": student.course_id,
            "grade": student.grade,
            "marks": str(student.marks),
        }
        FileHandler.write_to_csv(file_path, row, fieldnames=Student.FIELDS)
        print(f"Student {student.first_name} {student.last_name} added successfully!")

    @staticmethod
    def delete_student(email, file_path: str = None):
        file_path = file_path or Student.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("email") == email for r in rows):
            raise ValueError(f"No student found with email: {email}")
        FileHandler.delete_from_csv(file_path, "email", email)
        print(f"Student with email {email} deleted successfully!")

    @staticmethod
    def update_student(email, updated_data, file_path: str = None):
        file_path = file_path or Student.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("email") == email for r in rows):
            raise ValueError(f"No student found with email: {email}")
        if "marks" in updated_data:
            try:
                updated_data["marks"] = int(updated_data["marks"])
            except Exception:
                pass
        FileHandler.update_csv(file_path, "email", email, updated_data)
        print(f"Student with email {email} updated successfully!")

    
    @staticmethod
    def course_stats(course_id: str, file_path: str = None):
        """
        Return stats for a given course_id:
        count, average, median, min, max.
        If no marks found, return None.
        """
        file_path = file_path or Student.DATA_FILE
        rows = FileHandler.read_all(file_path)

        marks = []
        for r in rows:
            if r.get("course_id") == course_id and r.get("marks") not in (None, "", "None"):
                try:
                    marks.append(int(r["marks"]))
                except ValueError:
                    pass

        if not marks:
            return None

        count = len(marks)
        avg = round(sum(marks) / count, 2)
        med = median(marks)
        mn = min(marks)
        mx = max(marks)

        return {
            "course_id": course_id,
            "count": count,
            "average": avg,
            "median": med,
            "min": mn,
            "max": mx,
        }


    # LOAD, SEARCH, SORT, TIMING
    @staticmethod
    def read_all(file_path: str = None):
        file_path = file_path or Student.DATA_FILE
        return FileHandler.read_all(file_path)

    @staticmethod
    def sort_students(by: str = "marks", descending: bool = False, file_path: str = None):
        file_path = file_path or Student.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if by == "marks":
            rows.sort(key=lambda r: int(r["marks"]), reverse=descending)
        elif by == "name":
            rows.sort(
                key=lambda r: (r["last_name"].casefold(), r["first_name"].casefold()),
                reverse=descending,
            )
        else:
            rows.sort(key=lambda r: r["email"].casefold(), reverse=descending)
        return rows

    @staticmethod
    def search_by_email(email: str, file_path: str = None):
        file_path = file_path or Student.DATA_FILE
        rows = FileHandler.read_all(file_path)
        t0 = time.perf_counter()
        found = next((r for r in rows if r["email"] == email), None)
        t1 = time.perf_counter()
        return found, (t1 - t0)

    @staticmethod
    def search_by_name(keyword: str, file_path: str = None):
        file_path = file_path or Student.DATA_FILE
        rows = FileHandler.read_all(file_path)
        kw = keyword.casefold()
        t0 = time.perf_counter()
        hits = [
            r
            for r in rows
            if kw in r["first_name"].casefold() or kw in r["last_name"].casefold()
        ]
        t1 = time.perf_counter()
        return hits, (t1 - t0)
