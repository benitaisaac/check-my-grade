# utils/file_handler.py
import csv
import os
from typing import List, Dict, Iterable, Optional

class FileHandler:
    @staticmethod
    def read_all(file_path: str) -> List[Dict[str, str]]:
        if not os.path.isfile(file_path):
            return []
        with open(file_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    @staticmethod
    def write_header_if_missing(file_path: str, fieldnames: Iterable[str]) -> None:
        # If file missing -> create with header
        if not os.path.isfile(file_path):
            os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
            return

        # If file exists but header missing -> rewrite with header (rare)
        with open(file_path, "r", newline="") as f:
            first_line = f.readline().strip()
        if not first_line:
            with open(file_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

    @staticmethod
    def _current_header(file_path: str) -> Optional[List[str]]:
        if not os.path.isfile(file_path):
            return None
        with open(file_path, "r", newline="") as f:
            line = f.readline().strip()
            return line.split(",") if line else None

    @staticmethod
    def write_to_csv(file_path: str, data: Dict[str, object], fieldnames: Optional[Iterable[str]] = None) -> None:
        # Preserve a stable column order
        header = fieldnames or FileHandler._current_header(file_path) or list(data.keys())
        FileHandler.write_header_if_missing(file_path, header)
        with open(file_path, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writerow(data)

    @staticmethod
    def delete_from_csv(file_path: str, key: str, value: str) -> None:
        rows = FileHandler.read_all(file_path)
        if not rows:
            return
        header = rows[0].keys()
        kept = [r for r in rows if r.get(key) != value]
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(kept)

    @staticmethod
    def update_csv(file_path: str, key: str, value: str, new_data: Dict[str, object]) -> None:
        rows = FileHandler.read_all(file_path)
        if not rows:
            return
        header = rows[0].keys()
        out = []
        for r in rows:
            if r.get(key) == value:
                r.update({k: str(v) for k, v in new_data.items()})
            out.append(r)
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(out)
