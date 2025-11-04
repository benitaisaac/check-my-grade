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
        self.marks = marks

    def display_records(self):
        print(f"{self.first_name} {self.last_name} - {self.course_id} - {self.grade} ({self.marks})")

    @staticmethod
    def add_new_student(student, file_path: str = None):
        file_path = file_path or Student.DATA_FILE

        # Read all existing students
        students = FileHandler.read_all(file_path)

        # Check if this email already exists
        for row in students:
            if row.get("email") == student.email:
                raise ValueError("Email already exists")

        # Write in a stable column order
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
        """
        Delete a student record by email.
        Raises a ValueError if the email is not found.
        """
        file_path = file_path or Student.DATA_FILE
        students = FileHandler.read_all(file_path)

        exists = any(row.get("email") == email for row in students)
        if not exists:
            raise ValueError(f"No student found with email: {email}")

        FileHandler.delete_from_csv(file_path, "email", email)
        print(f"Student with email {email} deleted successfully!")

    # all methods above will be utilized by admins (NOT students)
    @staticmethod
    def update_student(email, updated_data, file_path: str = None):
        """
        Update a student record by email.
        Example: {"grade": "B", "marks": 85}
        Raises ValueError if email not found.
        """
        file_path = file_path or Student.DATA_FILE
        students = FileHandler.read_all(file_path)

        exists = any(row.get("email") == email for row in students)
        if not exists:
            raise ValueError(f"No student found with email: {email}")

        FileHandler.update_csv(file_path, "email", email, updated_data)
        print(f"Student with email {email} updated successfully!")

    # method utilized by a student user 
    @staticmethod
    def check_my_grades(email, course_id=None):
        file_path = Student.DATA_FILE
        rows = FileHandler.read_all(file_path)
        my_rows = [r for r in rows if r.get("email") == email]
        if not my_rows:
            raise ValueError(f"No records found for email: {email}")
        if course_id is not None:
            for r in my_rows:
                if r.get("course_id") == course_id:
                    return r.get("grade")
            raise ValueError(f"No record for course {course_id} for {email}")
        return [(r.get("course_id"), r.get("grade")) for r in my_rows]

    # method utilized by a student user 
    @staticmethod
    def check_my_marks(email, course_id=None):
        file_path = Student.DATA_FILE
        rows = FileHandler.read_all(file_path)
        my_rows = [r for r in rows if r.get("email") == email]
        if not my_rows:
            raise ValueError(f"No records found for email: {email}")

        def to_int_if_possible(v):
            try:
                return int(v)
            except Exception:
                return v

        if course_id is not None:
            for r in my_rows:
                if r.get("course_id") == course_id:
                    return to_int_if_possible(r.get("marks"))
            raise ValueError(f"No record for course {course_id} for {email}")

        return [(r.get("course_id"), to_int_if_possible(r.get("marks"))) for r in my_rows]
