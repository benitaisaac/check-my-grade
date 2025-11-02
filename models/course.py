from utils.file_handler import FileHandler

class Course:
    DATA_FILE = "data/courses.csv"
    FIELDS = ["course_id", "name", "description"]

    def __init__(self, course_id, name, description):
        self.course_id = course_id
        self.name = name
        self.description = description

    def display_courses(self):
        print(f"{self.course_id}: {self.name} - {self.description}")

    # use static method so we do not need to call on an instance
    # we can call it on an object 
    @staticmethod
    def add_new_course(course, file_path: str = None):
        file_path = file_path or Course.DATA_FILE
        rows = FileHandler.read_all(file_path)
        # Make sure that this course does not already exist
        if any(r.get("course_id") == course.course_id for r in rows):
            raise ValueError("Course ID already exists")

        # Create the row to be added to the csv file
        row = {
            "course_id": course.course_id,
            "name": course.name,
            "description": course.description,
        }
        # add to csv file 
        FileHandler.write_to_csv(file_path, row, fieldnames=Course.FIELDS)
        print(f"Course {course.course_id} added successfully!")

    @staticmethod
    def delete_course(course_id, file_path: str = None):
        file_path = file_path or Course.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("course_id") == course_id for r in rows):
            raise ValueError(f"No course found with id: {course_id}")

        FileHandler.delete_from_csv(file_path, "course_id", course_id)
        print(f"Course {course_id} deleted successfully!")

    @staticmethod
    def update_course(course_id, updated_data, file_path: str = None):
        file_path = file_path or Course.DATA_FILE
        rows = FileHandler.read_all(file_path)
        # make sure that the course exists
        if not any(r.get("course_id") == course_id for r in rows):
            raise ValueError(f"No course found with id: {course_id}")

        # update course in csv file 
        FileHandler.update_csv(file_path, "course_id", course_id, updated_data)
        print(f"Course {course_id} updated successfully!")
