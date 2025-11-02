from utils.file_handler import FileHandler
from utils.encryption import encrypt, decrypt

class LoginUser:
    DATA_FILE = "data/login.csv"
    FIELDS = ["email", "password", "role"]

    def __init__(self, email, password, role):
        self.email = email
        self.password = password  # plain in memory; will be encrypted on write
        self.role = role

    @staticmethod
    def add_user(user, file_path: str = None):
        """
        Adds a user with encrypted password. Enforces unique email.
        """
        file_path = file_path or LoginUser.DATA_FILE
        rows = FileHandler.read_all(file_path)

        if any(r.get("email") == user.email for r in rows):
            raise ValueError("Email already exists")

        row = {
            "email": user.email,
            "password": encrypt(user.password),
            "role": user.role,
        }
        FileHandler.write_to_csv(file_path, row, fieldnames=LoginUser.FIELDS)
        print(f"User {user.email} added successfully!")

    @staticmethod
    def delete_user(email, file_path: str = None):
        file_path = file_path or LoginUser.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("email") == email for r in rows):
            raise ValueError(f"No user found with email: {email}")

        FileHandler.delete_from_csv(file_path, "email", email)
        print(f"User {email} deleted successfully!")

    @staticmethod
    def update_user(email, updated_data, file_path: str = None):
        """
        Updates fields; if 'password' is present it will be re-encrypted.
        """
        file_path = file_path or LoginUser.DATA_FILE
        rows = FileHandler.read_all(file_path)
        if not any(r.get("email") == email for r in rows):
            raise ValueError(f"No user found with email: {email}")

        if "password" in updated_data:
            updated_data = dict(updated_data)  # shallow copy
            updated_data["password"] = encrypt(updated_data["password"])

        FileHandler.update_csv(file_path, "email", email, updated_data)
        print(f"User {email} updated successfully!")

    @staticmethod
    def authenticate(email, password, file_path: str = None) -> bool:
        """
        Returns True if a user exists and password matches.
        """
        file_path = file_path or LoginUser.DATA_FILE
        rows = FileHandler.read_all(file_path)
        for r in rows:
            if r.get("email") == email:
                try:
                    return decrypt(r.get("password", "")) == password
                except Exception:
                    return False
        return False

    def login(self, entered_password) -> bool:
        return self.password == entered_password
