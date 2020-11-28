from authenticate import Login
from signup import Signup
from logger import ConfigureLogs

class MainUi():

    def ask_user(self):
        print("Enter 0 to Login\nEnter 1 to SignUp")
        option = input("your option: ")
        if option == '0':
            #redirect to login
            logger = ConfigureLogs().configure_log("general")
            Login().user_login(logger)
        elif option == '1':
            #redirect to signup
            logger = ConfigureLogs().configure_log("general")
            Signup().signup_user(logger)
        else:
            print('enter correct option')

MainUi().ask_user()

