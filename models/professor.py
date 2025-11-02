from utils.file_handler import FileHandler

class Professor:
    DATA_FILE = "data/professors.csv"
    FIELDS = ["prof_id", "name", "rank", "course_id"]

    def __init__(self, prof_id, name, rank, course_id):
        self.prof_id = prof_id
        self.name = name
        self.rank = rank
        self.course_id = course_id

    def professors_details(self):
        print(f"{self.name} ({self.rank}) - {self.course_id}")

    @staticmethod
    def add_new_professor(professor, file_path: str = None):
        file_path = file_path or Professor.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if any(r.get("prof_id") == professor.prof_id for r in rows):
            raise ValueError("Professor ID already exists")

        row = {
            "prof_id": professor.prof_id,
            "name": professor.name,
            "rank": professor.rank,
            "course_id": professor.course_id,
        }
        FileHandler.write_to_csv(file_path, row, fieldnames=Professor.FIELDS)
        print(f"Professor {professor.prof_id} added successfully!")

    @staticmethod
    def delete_professor(prof_id, file_path: str = None):
        file_path = file_path or Professor.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("prof_id") == prof_id for r in rows):
            raise ValueError(f"No professor found with id: {prof_id}")

        FileHandler.delete_from_csv(file_path, "prof_id", prof_id)
        print(f"Professor {prof_id} deleted successfully!")

    @staticmethod
    def update_professor(prof_id, updated_data, file_path: str = None):
        file_path = file_path or Professor.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("prof_id") == prof_id for r in rows):
            raise ValueError(f"No professor found with id: {prof_id}")

        FileHandler.update_csv(file_path, "prof_id", prof_id, updated_data)
        print(f"Professor {prof_id} updated successfully!")
