
from utils.file_handler import FileHandler
from models.student import Student
from models.course import Course
from models.professor import Professor
from models.login_user import LoginUser

def ensure_headers():
    """Make sure all CSVs exist with headers before we start."""
    FileHandler.write_header_if_missing(Student.DATA_FILE, Student.FIELDS)
    FileHandler.write_header_if_missing(Course.DATA_FILE, Course.FIELDS)
    FileHandler.write_header_if_missing(Professor.DATA_FILE, Professor.FIELDS)
    FileHandler.write_header_if_missing(LoginUser.DATA_FILE, LoginUser.FIELDS)

def get_user_role(email: str):
    """Lookup role for user."""
    rows = FileHandler.read_all(LoginUser.DATA_FILE)
    for r in rows:
        if r.get("email") == email:
            return r.get("role")
    return None

# Student Menu (for admin) 
def admin_students_menu():
    while True:
        print("\n=== Admin: Students ===")
        print("1) Add student")
        print("2) List students")
        print("3) Update student")
        print("4) Delete student")
        print("5) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            email = input("Email: ").strip()
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            course_id = input("Course ID (e.g., DATA200): ").strip()
            grade = input("Grade (e.g., A): ").strip()
            marks = input("Marks (0–100): ").strip()
            try:
                s = Student(email, first, last, course_id, grade, marks)
                Student.add_new_student(s)
                print("Student added.")
            except ValueError as e:
                print(e)

        elif choice == "2":
            rows = FileHandler.read_all(Student.DATA_FILE)
            if not rows:
                print("No students yet.")
            else:
                for r in rows:
                    print(r)

        elif choice == "3":
            email = input("Email to update: ").strip()
            new_grade = input("New grade (blank to skip): ").strip()
            new_marks = input("New marks (blank to skip): ").strip()
            updated = {}
            if new_grade:
                updated["grade"] = new_grade
            if new_marks:
                updated["marks"] = new_marks
            if not updated:
                print("Nothing to update.")
                continue
            try:
                Student.update_student(email, updated)
                print("Student updated.")
            except ValueError as e:
                print(e)

        elif choice == "4":
            email = input("Email to delete: ").strip()
            try:
                Student.delete_student(email)
                print("Student deleted.")
            except ValueError as e:
                print(e)

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# Admin Menu 
def admin_courses_menu():
    while True:
        print("\n=== Admin: Courses ===")
        print("1) Add course")
        print("2) List courses")
        print("3) Update course")
        print("4) Delete course")
        print("5) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            course_id = input("Course ID: ").strip()
            name = input("Name: ").strip()
            desc = input("Description: ").strip()
            try:
                c = Course(course_id, name, desc)
                Course.add_new_course(c)
                print("Course added.")
            except ValueError as e:
                print(e)

        elif choice == "2":
            rows = FileHandler.read_all(Course.DATA_FILE)
            if not rows:
                print("No courses yet.")
            else:
                for r in rows:
                    print(r)

        elif choice == "3":
            course_id = input("Course ID to update: ").strip()
            name = input("New name (blank to skip): ").strip()
            desc = input("New description (blank to skip): ").strip()
            updated = {}
            if name:
                updated["name"] = name
            if desc:
                updated["description"] = desc
            if not updated:
                print("Nothing to update.")
                continue
            try:
                Course.update_course(course_id, updated)
                print("Course updated.")
            except ValueError as e:
                print(e)

        elif choice == "4":
            course_id = input("Course ID to delete: ").strip()
            try:
                Course.delete_course(course_id)
                print("Course deleted.")
            except ValueError as e:
                print(e)

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# Admin Professors menu 
def admin_professors_menu():
    while True:
        print("\n=== Admin: Professors ===")
        print("1) Add professor")
        print("2) List professors")
        print("3) Update professor")
        print("4) Delete professor")
        print("5) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            prof_id = input("Professor ID: ").strip()
            name = input("Name: ").strip()
            rank = input("Rank: ").strip()
            course_id = input("Course ID: ").strip()
            try:
                p = Professor(prof_id, name, rank, course_id)
                Professor.add_new_professor(p)
                print("Professor added.")
            except ValueError as e:
                print(e)

        elif choice == "2":
            rows = FileHandler.read_all(Professor.DATA_FILE)
            if not rows:
                print("No professors yet.")
            else:
                for r in rows:
                    print(r)

        elif choice == "3":
            prof_id = input("Professor ID to update: ").strip()
            name = input("New name (blank to skip): ").strip()
            rank = input("New rank (blank to skip): ").strip()
            course_id = input("New course ID (blank to skip): ").strip()
            updated = {}
            if name:
                updated["name"] = name
            if rank:
                updated["rank"] = rank
            if course_id:
                updated["course_id"] = course_id
            if not updated:
                print("Nothing to update.")
                continue
            try:
                Professor.update_professor(prof_id, updated)
                print("Professor updated.")
            except ValueError as e:
                print(e)

        elif choice == "4":
            prof_id = input("Professor ID to delete: ").strip()
            try:
                Professor.delete_professor(prof_id)
                print("Professor deleted.")
            except ValueError as e:
                print(e)

        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# Professor Menu 
def professor_menu():
    while True:
        print("\n=== Professor Menu ===")
        print("1) List all students")
        print("2) Update a student's grade/marks")
        print("3) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            rows = FileHandler.read_all(Student.DATA_FILE)
            if not rows:
                print("No students yet.")
            else:
                for r in rows:
                    print(r)

        elif choice == "2":
            email = input("Student email to update: ").strip()
            new_grade = input("New grade (blank to skip): ").strip()
            new_marks = input("New marks (blank to skip): ").strip()
            updated = {}
            if new_grade:
                updated["grade"] = new_grade
            if new_marks:
                updated["marks"] = new_marks
            if not updated:
                print("Nothing to update.")
                continue
            try:
                Student.update_student(email, updated)
                print("Student updated.")
            except ValueError as e:
                print(e)

        elif choice == "3":
            break
        else:
            print("Invalid choice.")

# Student menu 
def student_menu(current_email: str):
    while True:
        print("\n=== Student Menu ===")
        print("1) Check my marks")
        print("2) Check my grades")
        print("3) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            course = input("Enter course ID (blank = all): ").strip() or None
            try:
                result = Student.check_my_marks(current_email, course)
                if isinstance(result, list):
                    print("\nYour marks:")
                    for cid, mark in result:
                        print(f"{cid}: {mark}")
                else:
                    print(f"\nMarks: {result}")
            except ValueError as e:
                print(e)

        elif choice == "2":
            course = input("Enter course ID (blank = all): ").strip() or None
            try:
                result = Student.check_my_grades(current_email, course)
                if isinstance(result, list):
                    print("\nYour grades:")
                    for cid, grade in result:
                        print(f"{cid}: {grade}")
                else:
                    print(f"\nGrade: {result}")
            except ValueError as e:
                print(e)

        elif choice == "3":
            break
        else:
            print("Invalid choice.")

# Admin Dashboard 
def admin_main_menu():
    while True:
        print("\n===== Admin Dashboard =====")
        print("1) Students")
        print("2) Courses")
        print("3) Professors")
        print("4) Logout")
        choice = input("Choose: ").strip()

        if choice == "1":
            admin_students_menu()
        elif choice == "2":
            admin_courses_menu()
        elif choice == "3":
            admin_professors_menu()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

# App entry 
def main():
    ensure_headers()

    print("===== CheckMyGrade Login =====")
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    if not LoginUser.authenticate(email, password):
        print("Invalid email or password.")
        return

    role = get_user_role(email)
    if role is None:
        print("No role found for this user.")
        return

    print(f"Logged in as {role}")

    if role == "admin":
        admin_main_menu()
    elif role == "professor":
        professor_menu()
    elif role == "student":
        student_menu(email)
    else:
        print("Unknown role. Please contact admin.")

if __name__ == "__main__":
    main()
