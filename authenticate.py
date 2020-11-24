import json
from parse import ParseQuery

class Login():

    def user_login(self):
        print("-------------------Login----------------------")
        username = input("enter username: ")
        password = input("enter password: ")
        with open("user_details.json") as user_details:
            data = json.load(user_details)
            usrs = data['User_Details']
            flag = 0
            print(usrs)
            for user in usrs:
                if user['username'] == username and user['password'] == password:
                    flag = 0
                    break
                else:
                    flag = 1
            if flag == 1:
                print("enter valid username and password")
            else:
                print("User authenticated")
                if username == 'root':
                    grant = input("enter the username to whom you want to grant permissions: ")
                    with open("user_details.json") as user_details:
                        data = json.load(user_details)
                        usrs = data['User_Details']
                        for user in usrs:
                            if user['username'] == grant.lower():
                                permissions = user['granted_privileges']
                                print('granted permissions', permissions)
                                permit = input("enter the privilege you want to enable to this user: ")
                                permissions.append(permit.lower())
                        with open("user_details.json",'w') as usr_details:
                            json.dump(data,usr_details,indent=4)      
                else:               
                    query= input("enter query in SQL to process: ")
                    ParseQuery().parse_query(username,query)
                
                

            