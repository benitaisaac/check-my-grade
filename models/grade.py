from utils.file_handler import FileHandler

class Grade:
    DATA_FILE = "data/grades.csv"
    FIELDS = ["grade_id", "grade", "marks_range"]  

    def __init__(self, grade_id, grade, marks_range):
        self.grade_id = grade_id
        self.grade = grade
        self.marks_range = marks_range

    def display_grade_report(self):
        print(f"Grade {self.grade} -> Marks Range: {self.marks_range}")

    @staticmethod
    def add_new_grade(grade, file_path: str = None):
        file_path = file_path or Grade.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if any(r.get("grade_id") == grade.grade_id for r in rows):
            raise ValueError("Grade ID already exists")

        row = {
            "grade_id": grade.grade_id,
            "grade": grade.grade,
            "marks_range": grade.marks_range,
        }
        FileHandler.write_to_csv(file_path, row, fieldnames=Grade.FIELDS)
        print(f"Grade {grade.grade_id} added successfully!")

    @staticmethod
    def delete_grade(grade_id, file_path: str = None):
        file_path = file_path or Grade.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("grade_id") == grade_id for r in rows):
            raise ValueError(f"No grade found with id: {grade_id}")

        FileHandler.delete_from_csv(file_path, "grade_id", grade_id)
        print(f"Grade {grade_id} deleted successfully!")

    @staticmethod
    def update_grade(grade_id, updated_data, file_path: str = None):
        file_path = file_path or Grade.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("grade_id") == grade_id for r in rows):
            raise ValueError(f"No grade found with id: {grade_id}")

        FileHandler.update_csv(file_path, "grade_id", grade_id, updated_data)
        print(f"Grade {grade_id} updated successfully!")
