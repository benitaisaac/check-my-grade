# main.py
import time
from utils.file_handler import FileHandler
from models.student import Student
from models.course import Course
from models.professor import Professor
from models.login_user import LoginUser

# Make sure headers exist 
def ensure_headers():
    FileHandler.write_header_if_missing(Student.DATA_FILE, Student.FIELDS)
    FileHandler.write_header_if_missing(Course.DATA_FILE, Course.FIELDS)
    FileHandler.write_header_if_missing(Professor.DATA_FILE, Professor.FIELDS)
    FileHandler.write_header_if_missing(LoginUser.DATA_FILE, LoginUser.FIELDS)
def seed_demo_data():
    """
    One-time seed for demo. Run once, then comment out.
    Safe: only adds if CSVs are (nearly) empty.
    """
    # Seed courses
    if not FileHandler.read_all(Course.DATA_FILE):
        Course.add_new_course(Course("DATA200", "Data Foundations", "Intro to data"))
        Course.add_new_course(Course("DATA210", "Database Systems", "SQL and design"))
        Course.add_new_course(Course("DATA220", "Algorithms", "Core algorithms"))

    # Seed professors (one per course)
    if not FileHandler.read_all(Professor.DATA_FILE):
        Professor.add_new_professor(Professor("P001", "Ada Lovelace", "Associate", "DATA200"))
        Professor.add_new_professor(Professor("P002", "Alan Turing", "Full", "DATA210"))
        Professor.add_new_professor(Professor("P003", "Grace Hopper", "Associate", "DATA220"))

    # Seed login users (admin + one professor + one student)
    from models.login_user import LoginUser
    if not FileHandler.read_all(LoginUser.DATA_FILE):
        LoginUser.add_user(LoginUser("admin@mycsu.edu", "password1", "admin"))
        LoginUser.add_user(LoginUser("prof@mycsu.edu", "profpass", "professor"))
        LoginUser.add_user(LoginUser("student1@mycsu.edu", "studpass", "student"))

    # Seed students (only if very few exist)
    existing_students = FileHandler.read_all(Student.DATA_FILE)
    if len(existing_students) < 10:
        # Add 60 students across 3 courses with varied marks
        for i in range(60):
            course_id = "DATA200" if i % 3 == 0 else ("DATA210" if i % 3 == 1 else "DATA220")
            grade = "A" if i % 10 < 3 else ("B" if i % 10 < 7 else "C")
            marks = (i * 7) % 101  # spreads 0..100
            s = Student(
                f"student{i}@mycsu.edu", f"First{i}", f"Last{i}",
                course_id, grade, marks
            )
            try:
                Student.add_new_student(s)
            except ValueError:
                pass  # skip duplicates if you re-run accidentally


# Login helpers
def get_user_role(email: str) -> str:
    """Return role for a given email from login.csv (or '' if not found)."""
    rows = FileHandler.read_all(LoginUser.DATA_FILE)
    for r in rows:
        if r.get("email") == email:
            return r.get("role", "")
    return ""

def login_flow():
    """Prompt for email/password and authenticate up to 3 attempts."""
    attempts = 0
    while attempts < 3:
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        if LoginUser.authenticate(email, password):
            role = get_user_role(email)
            if role:
                print(f"Login successful. Role: {role}")
                return email, role
            else:
                print("User found but role missing. Contact admin.")
                return None, None
        else:
            print("Invalid credentials. Try again.")
            attempts += 1
    print("Too many failed attempts.")
    return None, None

# Students: Search & Sort submenu (Admin portal)
def menu_students_search_sort():
    while True:
        print("\n=== Students: Search & Sort ===")
        print("1) Search by email (timed)")
        print("2) Search by name contains (timed)")
        print("3) Sort by marks ASC")
        print("4) Sort by marks DESC")
        print("5) Sort by name ASC (Last, First)")
        print("6) Sort by name DESC (Last, First)")
        print("7) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            email = input("Email to search: ").strip()
            row, elapsed = Student.search_by_email(email)
            print(f"Time: {elapsed:.6f} s")
            print("Result:", row if row else "Not found")

        elif choice == "2":
            kw = input("Name contains: ").strip()
            rows, elapsed = Student.search_by_name(kw)
            print(f"Time: {elapsed:.6f} s")
            print(f"Found {len(rows)} record(s).")
            for r in rows[:10]:
                print(r)
            if len(rows) > 10:
                print(f"... and {len(rows)-10} more")

        elif choice in ("3", "4", "5", "6"):
            if choice == "3":
                by, desc = "marks", False
            elif choice == "4":
                by, desc = "marks", True
            elif choice == "5":
                by, desc = "name", False
            else:
                by, desc = "name", True

            t0 = time.perf_counter()
            rows = Student.sort_students(by=by, descending=desc)
            t1 = time.perf_counter()
            print(f"Sort time: {(t1 - t0):.6f} s")
            for r in rows[:10]:
                print(r)

        elif choice == "7":
            break
        else:
            print("Invalid choice.")

# Full CRUD Menus (Admin)
def menu_students_admin():
    while True:
        print("\n=== Students (Admin) ===")
        print("1) Add student")
        print("2) List students")
        print("3) Update student")
        print("4) Delete student")
        print("5) Search & Sort (timed)")
        print("6) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            email = input("Email: ").strip()
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            course = input("Course ID: ").strip()
            grade = input("Grade: ").strip()
            marks = input("Marks: ").strip()
            try:
                s = Student(email, first, last, course, grade, marks)
                Student.add_new_student(s)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            rows = FileHandler.read_all(Student.DATA_FILE)
            if not rows:
                print("No students yet.")
            else:
                for r in rows:
                    print(r)

        elif choice == "3":
            email = input("Email to update: ").strip()
            grade = input("New grade (blank to skip): ").strip()
            marks = input("New marks (blank to skip): ").strip()
            data = {}
            if grade:
                data["grade"] = grade
            if marks:
                data["marks"] = marks
            try:
                if data:
                    Student.update_student(email, data)
                else:
                    print("Nothing to update.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            email = input("Email to delete: ").strip()
            try:
                Student.delete_student(email)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            menu_students_search_sort()

        elif choice == "6":
            break
        else:
            print("Invalid choice.")

def menu_courses_admin():
    while True:
        print("\n=== Courses (Admin) ===")
        print("1) Add course")
        print("2) List courses")
        print("3) Update course")
        print("4) Delete course")
        print("5) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            cid = input("Course ID: ").strip()
            name = input("Course name: ").strip()
            desc = input("Description: ").strip()
            try:
                c = Course(cid, name, desc)
                Course.add_new_course(c)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            rows = FileHandler.read_all(Course.DATA_FILE)
            if not rows:
                print("No courses yet.")
            else:
                for r in rows:
                    print(r)

        elif choice == "3":
            cid = input("Course ID to update: ").strip()
            new_name = input("New name: ").strip()
            new_desc = input("New description: ").strip()
            data = {}
            if new_name:
                data["name"] = new_name
            if new_desc:
                data["description"] = new_desc
            try:
                if data:
                    Course.update_course(cid, data)
                else:
                    print("Nothing to update.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            cid = input("Course ID to delete: ").strip()
            try:
                Course.delete_course(cid)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def menu_professors_admin():
    while True:
        print("\n=== Professors (Admin) ===")
        print("1) Add professor")
        print("2) List professors")
        print("3) Update professor")
        print("4) Delete professor")
        print("5) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            pid = input("Professor ID: ").strip()
            name = input("Name: ").strip()
            rank = input("Rank: ").strip()
            cid = input("Course ID: ").strip()
            try:
                p = Professor(pid, name, rank, cid)
                Professor.add_new_professor(p)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            rows = FileHandler.read_all(Professor.DATA_FILE)
            if not rows:
                print("No professors yet.")
            else:
                for r in rows:
                    print(r)

        elif choice == "3":
            pid = input("Professor ID to update: ").strip()
            new_name = input("New name: ").strip()
            new_rank = input("New rank: ").strip()
            new_course = input("New course_id: ").strip()
            data = {}
            if new_name:
                data["name"] = new_name
            if new_rank:
                data["rank"] = new_rank
            if new_course:
                data["course_id"] = new_course
            try:
                if data:
                    Professor.update_professor(pid, data)
                else:
                    print("Nothing to update.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            pid = input("Professor ID to delete: ").strip()
            try:
                Professor.delete_professor(pid)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# Professor Portal (limited)
def menu_professor_portal(email: str):
    """
    Professor portal:
    - List ALL students
    - List students by course_id
    - Search student by email (timed)
    - Update a student's grade/marks
    - Course stats (avg/median/min/max)
    """
    while True:
        print("\n=== Professor Portal ===")
        print("1) List ALL students")
        print("2) List students by course_id")
        print("3) Search student by email (timed)")
        print("4) Update student grade/marks")
        print("5) Course stats (avg/median/min/max)")
        print("6) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            rows = FileHandler.read_all(Student.DATA_FILE)
            if not rows:
                print("No students found.")
            else:
                for r in rows:
                    print(r)

        elif choice == "2":
            cid = input("Course ID: ").strip()
            rows = FileHandler.read_all(Student.DATA_FILE)
            filtered = [r for r in rows if r.get("course_id") == cid]
            if not filtered:
                print("No students for that course.")
            else:
                for r in filtered:
                    print(r)

        elif choice == "3":
            email_q = input("Student email to search: ").strip()
            row, elapsed = Student.search_by_email(email_q)
            print(f"Time: {elapsed:.6f} s")
            print("Result:", row if row else "Not found")

        elif choice == "4":
            target_email = input("Student email to update: ").strip()
            new_grade = input("New grade (blank to skip): ").strip()
            new_marks = input("New marks (blank to skip): ").strip()
            data = {}
            if new_grade:
                data["grade"] = new_grade
            if new_marks:
                data["marks"] = new_marks
            if not data:
                print("Nothing to update.")
                continue
            try:
                Student.update_student(target_email, data)
                print("Update successful.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            cid = input("Course ID for stats: ").strip()
            stats = Student.course_stats(cid)
            if not stats:
                print("No marks found for that course.")
            else:
                print("\n--- Course Stats ---")
                print(f"Course:   {stats['course_id']}")
                print(f"Count:    {stats['count']}")
                print(f"Average:  {stats['average']}")
                print(f"Median:   {stats['median']}")
                print(f"Min:      {stats['min']}")
                print(f"Max:      {stats['max']}")

        elif choice == "6":
            break
        else:
            print("Invalid choice.")



# Student Portal (limited)
def menu_student_portal(email: str):
    """
    Simple student portal:
    - View your own record
    """
    while True:
        print("\n=== Student Portal ===")
        print("1) View my record")
        print("2) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            rows = FileHandler.read_all(Student.DATA_FILE)
            me = next((r for r in rows if r.get("email") == email), None)
            print("Your record:", me if me else "Not found")
        elif choice == "2":
            break
        else:
            print("Invalid choice.")


# Admin Portal (full control + search/sort)
def menu_admin():
    while True:
        print("\n=== Admin Portal ===")
        print("1) Students")
        print("2) Courses")
        print("3) Professors")
        print("4) Search & Sort Students (timed)")
        print("5) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            menu_students_admin()
        elif choice == "2":
            menu_courses_admin()
        elif choice == "3":
            menu_professors_admin()
        elif choice == "4":
            menu_students_search_sort()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


# MAIN
def main():
    ensure_headers()
    # added a seed_demo_data to add synthetic data for average/median data purposes 
    # seed_demo_data()

    while True:
        print("\n===== CheckMyGrade =====")
        print("1) Login")
        print("2) Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            email, role = login_flow()
            if not email:
                continue

            if role == "admin":
                menu_admin()
            elif role == "professor":
                menu_professor_portal(email)
            elif role == "student":
                menu_student_portal(email)
            else:
                print("Unknown role. Contact admin.")

        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
