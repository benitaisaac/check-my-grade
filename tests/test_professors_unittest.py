import os
import shutil
import tempfile
import unittest

from models.professor import Professor
from utils.file_handler import FileHandler

class TestProfessors(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.tmpdir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.file_path = os.path.join(self.data_dir, "professors.csv")
        with open(self.file_path, "w") as f:
            f.write(",".join(Professor.FIELDS) + "\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_add_update_delete_professor(self):
        # ADD
        p = Professor("P001", "Ada Lovelace", "Associate", "DATA200")
        Professor.add_new_professor(p, file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["prof_id"], "P001")

        # UPDATE
        Professor.update_professor("P001", {"rank": "Full"}, file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(rows[0]["rank"], "Full")

        # DELETE
        Professor.delete_professor("P001", file_path=self.file_path)
        rows = FileHandler.read_all(self.file_path)
        self.assertEqual(len(rows), 0)
