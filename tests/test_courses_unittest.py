import os
import shutil
import tempfile
import unittest

from models.course import Course
from utils.file_handler import FileHandler

class TestCourses(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.tmpdir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.file_path = os.path.join(self.data_dir, "courses.csv")
        with open(self.file_path, "w") as f:
            f.write(",".join(Course.FIELDS) + "\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_add_update_delete_course(self):
        # ADD
        c = Course("DATA200", "Data Foundations", "Intro to data")
        Course.add_new_course(c, file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["course_id"], "DATA200")

        # UPDATE
        Course.update_course("DATA200", {"name": "Data Fundamentals"}, file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(rows[0]["name"], "Data Fundamentals")

        # DELETE
        Course.delete_course("DATA200", file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(len(rows), 0)
