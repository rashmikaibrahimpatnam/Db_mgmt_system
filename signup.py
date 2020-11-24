from authenticate import Login
import re
import json
import os.path

class Signup():        

    def validate_username(self,uname):
        if uname.isalpha():
            print("valid username")
            return True
        else:
            print("enter a username with only alphabets")
            return False

    def validate_password(self,pwd):
        check = 0
        while True:
            if(len(pwd)<8):
                check = 1
                break
            elif not re.search("[A-Z]",pwd):
                check = 1
                break
            elif not re.search("[a-z]",pwd):
                check = 1
                break
            elif not re.search("[0-9]",pwd):
                check = 1
                break
            elif not re.search("[@$#_*^&]",pwd):
                check = 1
                break
            elif re.search("\s",pwd):
                check = 1
                break
            else:
                print("password is valid")
                check = 0
                break
        if check == 1:
            print("Invalid password")
            return False

    def signup_user(self):
        print("-------------------Signup----------------------")
        uname = input("enter username: ")
        check_uname = self.validate_username(uname)
        if check_uname:
            pwd = input("enter pwd: ")
            check_pwd = self.validate_password(pwd=pwd)
            
            if check_pwd != False:
                file_exists = os.path.isfile("user_details.json")
                if file_exists:
                    with open("user_details.json") as user_details:
                        data = json.load(user_details)
                        usrs = data['User_Details']
                        detail_dict = {'username':uname,'password':pwd, 'granted_privileges' : ['select']}
                        usrs.append(detail_dict)
                        with open("user_details.json",'w') as usr_details:
                            json.dump(data,usr_details,indent=4)      
                        usr_details.close()          
                    user_details.close()
                    Login().user_login()
                else:
                    user_dict = {}
                    details = []
                    detail_dict = {'username':uname,'password':pwd,'granted_privileges' : ['select']}
                    details.append(detail_dict)
                    user_dict['User_Details'] = details
                    with open("user_details.json",'a') as user_details:
                        json.dump(user_dict,user_details,indent=4)
                    user_details.close()
                    Login().user_login()
        
            
