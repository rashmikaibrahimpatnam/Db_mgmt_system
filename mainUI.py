from authenticate import Login
from signup import Signup

class MainUi():
    def ask_user(self):
        print("Enter 0 to Login\nEnter 1 to SignUp")
        option = input("your option: ")
        if option == '0':
            #redirect to login
            Login().user_login()
        elif option == '1':
            #redirect to signup
            Signup().signup_user()
        else:
            print('enter correct option')

MainUi().ask_user()

