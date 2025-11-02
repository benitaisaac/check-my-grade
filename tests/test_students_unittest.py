import os
import shutil
import tempfile
import time
import unittest

from models.student import Student
from utils.file_handler import FileHandler

class TestStudents(unittest.TestCase):
    def setUp(self):
        # make a temp folder and a fresh CSV with header
        self.tmpdir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.tmpdir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.file_path = os.path.join(self.data_dir, "students.csv")

        # write header
        with open(self.file_path, "w") as f:
            f.write(",".join(Student.FIELDS) + "\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_add_update_delete_student(self):
        # ADD
        s = Student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", "A", 96)
        Student.add_new_student(s, file_path=self.file_path)

        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["email"], "sam@mycsu.edu")

        # UPDATE
        Student.update_student("sam@mycsu.edu", {"grade": "B", "marks": 85}, file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(rows[0]["grade"], "B")
        self.assertEqual(int(rows[0]["marks"]), 85)

        # DELETE
        Student.delete_student("sam@mycsu.edu", file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(len(rows), 0)

    def test_1000_records_search_and_sort(self):
        # Add 1000 students
        for i in range(1000):
            s = Student(
                f"student{i}@mycsu.edu",
                f"First{i}",
                f"Last{i}",
                "DATA200",
                "A",
                i % 101
            )
            Student.add_new_student(s, file_path=self.file_path)

        # load and simple search
        t_load_start = time.time()
        rows = FileHandler.read_all(self.file_path)
        t_load_end = time.time()

        t_search_start = time.time()
        target = "student999@mycsu.edu"
        found = None
        for r in rows:
            if r["email"] == target:
                found = r
                break
        t_search_end = time.time()

        print("\nLoad time:", round(t_load_end - t_load_start, 6), "sec")
        print("Search time:", round(t_search_end - t_search_start, 6), "sec")

        self.assertEqual(len(rows), 1000)
        self.assertIsNotNone(found)

        # sort by marks (ascending) and by email (descending)
        t_sort1_start = time.time()
        rows_by_marks_asc = sorted(rows, key=lambda r: int(r["marks"]))
        t_sort1_end = time.time()

        t_sort2_start = time.time()
        rows_by_email_desc = sorted(rows, key=lambda r: r["email"], reverse=True)
        t_sort2_end = time.time()

        print("Sort by marks (ASC):", round(t_sort1_end - t_sort1_start, 6), "sec")
        print("Sort by email (DESC):", round(t_sort2_end - t_sort2_start, 6), "sec")

        # quick correctness checks
        self.assertLessEqual(int(rows_by_marks_asc[0]["marks"]), int(rows_by_marks_asc[-1]["marks"]))
        self.assertGreaterEqual(rows_by_email_desc[0]["email"], rows_by_email_desc[-1]["email"])
