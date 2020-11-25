import re
from fetchdata import FindData
from deletedata import DeleteOp
from droptable import DropOp
from usedb import UseDb
import json

class ParseQuery():

    def login_status(self,username,dbname,logger):
        ask_usr = input("Enter 0 if you want to continue or any other key to exit: ")
        if ask_usr == '0':
            query= input("enter query in SQL to process: ")
            self.parse_query(username,dbname,query,logger)

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

    def create_use(self,username,query,logger):
        query = query.lower()
        words = query.split(' ')
        dbname = ''
        if words[0].lower() == 'create':
            dbname = words[1].strip(';')
            self.parse_createdb(username,dbname,logger)
        elif words[0].lower() == 'use':
            dbname = words[1].strip(';')
            self.parse_use(username,dbname,logger)
        logger.info("User {} has selected {} database".format(username,dbname))

    def parse_query(self,username,dbname,query,logger):
        query = query.lower()
        words = query.split(' ')
        check_permissions = self.check_permissions(username)
        if words[0] in check_permissions:
            if words[0].lower() == 'select':
                #select parsing
                self.parse_select(username,dbname,query,logger)
            elif words[0].lower() == 'delete':
                #delete parsing
                self.parse_delete(username,dbname,query,logger)
            elif words[0].lower() == 'drop':
                #drop table
                self.parse_drop(username,dbname,query,logger)
        else:
            print("no permissions granted")

    def parse_createdb(self,username,db_name,logger):
        status = UseDb().create_database(db_name)
        if status:
            query= input("enter query in SQL to process: ")
            self.parse_query(username,db_name,query,logger)
        else:
            query = input("give new db name with create")
            format = query.lower().split(' ')
            if len(format) == 2 and format[0] == 'create':
                self.create_use(username,query,logger)

    def parse_use(self,username,db_name,logger):
        status = UseDb().use_database(db_name)
        if status:
            query= input("enter query in SQL to process: ")
            self.parse_query(username,db_name,query,logger)
        else:
            query = input("create a new db with create: ")
            format = query.lower().split(' ')
            if len(format) == 2 and format[0] == 'create':
                self.create_use(username,query,logger)

    def parse_select(self,username,dbname,query,logger):
        query = query.lower()
        logger.info("parsing select query, {}".format(query))
        col = re.search('select(.+?)from',query).group(1)
        columns = col.strip().split(',')
        find = re.search('from(.+?)where',query)
        if find:
            table_name = find.group(1).strip().split(' ')
            pattern = re.compile('where(.*)')
            condition = pattern.findall(query)
            FindData().fetch_data(dbname,table_name[0],columns,condition[0].strip(';'),logger)
            self.login_status(username,dbname,logger)
        else:
            pattern = re.compile('from(.*)')
            table_name = pattern.findall(query)
            FindData().fetch_data(dbname,table_name[0].strip(';'),columns,logger=logger)
            self.login_status(username,dbname,logger)
    
    def parse_delete(self,username,dbname,query,logger):
        query = query.lower()
        logger.info("parsing delete query, {}".format(query))
        find = re.search('from(.+?)where',query)
        if find:
            table_name = find.group(1).strip().split(' ')
            pattern = re.compile('where(.*)')
            condition = pattern.findall(query)
            DeleteOp().delete_data(dbname,table_name[0],condition[0].strip(';'),logger)
            self.login_status(username,dbname,logger)

        else:
            pattern = re.compile('from(.*)')
            table_name = pattern.findall(query)
            DeleteOp().delete_data(dbname,table_name[0].strip(';'),logger=logger)
            self.login_status(username,dbname,logger)
            
    def parse_drop(self,username,dbname,query,logger):
        query = query.lower()
        logger.info("parsing drop query, {}".format(query))
        pattern = re.compile('table(.*)')
        table_name = pattern.findall(query)
        DropOp().drop_table(dbname,table_name[0].strip(';'),logger)
        self.login_status(username,dbname,logger)

        

