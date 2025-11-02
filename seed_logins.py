from models.login_user import LoginUser


try:
    LoginUser.add_user(LoginUser("admin1@mycsu.edu", "password1", "admin"))
    LoginUser.add_user(LoginUser("prof@mycsu.edu", "password2", "professor"))
    LoginUser.add_user(LoginUser("sam@mycsu.edu", "password3", "student"))
    print("Users added successfully to data/login.csv")
except ValueError as e:
    print(f" Value Error: {e}")
