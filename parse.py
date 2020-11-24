import re
from fetchdata import FindData
from deletedata import DeleteOp
import json

class ParseQuery():
    def login_status(self,username):
        ask_usr = input("Enter 0 if you want to continue or any other key to exit: ")
        if ask_usr == '0':
            query= input("enter query in SQL to process: ")
            self.parse_query(username,query)

    def check_permissions(self,username):
        with open("user_details.json") as user_details:
            data = json.load(user_details)
            usrs = data['User_Details']
            flag = 0
            print(usrs)
            for usr in usrs:
                if usr['username'] == username:
                    permissions = usr['granted_privileges']
                    return permissions


    def parse_query(self,username,query):
        check_permissions = self.check_permissions(username)
        words = query.split(' ')
        print(words)
        if words[0].lower() in check_permissions:
            if words[0].lower() == 'select':
                #select parsing
                self.parse_select(username,query)
            elif words[0].lower() == 'delete':
                #delete parsing
                self.parse_delete(username,query)
        else:
            print("no permissions granted")
               

    def parse_select(self,username,query):
        print(query)
        col = re.search('select(.+?)from',query).group(1)
        columns = col.strip().split(' ')
        find = re.search('from(.+?)where',query)
        if find:
            table_name = find.group(1).strip().split(' ')
            pattern = re.compile('where(.*)')
            condition = pattern.findall(query)
            FindData().fetch_data(username,table_name[0],columns,condition[0].strip(';'))
            self.login_status(username)
        else:
            pattern = re.compile('from(.*)')
            table_name = pattern.findall(query)
            FindData().fetch_data(username,table_name[0].strip(';'),columns)
            self.login_status(username)
    
    def parse_delete(self,username,query):
        print(query)
        find = re.search('from(.+?)where',query)
        if find:
            table_name = find.group(1).strip().split(' ')
            pattern = re.compile('where(.*)')
            condition = pattern.findall(query)
            DeleteOp().delete_data(username,table_name[0],condition[0].strip(';'))
            self.login_status(username)

        else:
            pattern = re.compile('from(.*)')
            table_name = pattern.findall(query)
            DeleteOp().delete_data(username,table_name[0].strip(';'))
            self.login_status(username)
            
        

