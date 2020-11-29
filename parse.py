import re
from fetchdata import FindData
from deletedata import DeleteOp
from droptable import DropOp
from usedb import UseDb
from create import CreatQuery
from insert import InsertQuery
import json
import os
from tabulate import tabulate
import pandas as pd
from ast import dump
import shutil

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
            for usr in usrs:
                if usr['username'] == username:
                    permissions = usr['granted_privileges']
                    return permissions

    def showdb(self,username,logger):
        files = os.listdir()
        print("-------------------List Of Databases----------------------")
        db_dict = {}
        lst_db = []
        for file in files:
            if file.endswith('_Tables.txt'):                
                lst_db.append(file[0:-11])
                db_dict['databases'] = lst_db
        databases = db_dict['databases']
        print(tabulate(pd.DataFrame(databases, columns=db_dict.keys()),headers = 'keys', tablefmt = 'psql'))
        query= input("use already created database or create a new one using sql query only: ")
        format = query.lower().split(' ')
        if len(format) == 2 and (format[0] == 'use' or format[0] == 'create'):
            self.create_use(username,query,logger)

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

    def parse_query(self,username,dbname,query,logger,fname=None):
        query = query.lower()
        words = query.split(' ')
        check_permissions = self.check_permissions(username)
        if words[0] in check_permissions:
            if words[0].lower() == 'select':
                #select parsing
                try:
                    self.parse_select(username,dbname,query,logger)
                except:
                    print("Error in your Select query!!! Please check syntax!!")
            elif words[0].lower() == 'delete':
                #delete parsing
                try:
                    self.parse_delete(username,dbname,query,logger,fname)
                except:
                    print("Error in your Delete query!!! Please check syntax!!")
            elif words[0].lower() == 'drop':
                #drop table
                try:
                    self.parse_drop(username,dbname,query,logger,fname)
                except:
                    print("Error in your drop query!!! Please check syntax!!")
            elif words[0].lower() == 'create':
                crtObj = CreatQuery()
                try:
                    crtObj.create_table(username,dbname,query,logger)
                    self.login_status(username, dbname, logger)
                except:
                    print("Error in your Create query!!! Please check syntax!!")
            elif words[0].lower() == 'insert':
                insertObj = InsertQuery()
                try:
                    insertObj.insert_row(username,dbname,query,logger)
                    self.login_status(username, dbname, logger)
                except:
                    print("Error in your Insert query!!! Please check syntax!!")
        else:
            print("no permissions granted")

    def parse_transactions(self,username,db_name,logger):
        query_list =[]
        file_exists = os.path.isfile("lock_details.json")
        if file_exists:
            with open("lock_details.json") as lock_details:
                data = json.load(lock_details)
                lock = data['Lock_Details']
                
                if lock['lock_acquired'] == True:
                    print("other user is already accessing the database")
                    return
                else:
                    detail_dict = {'lock_acquired': True,'username':username}
                    data['Lock_Details'] = detail_dict
                    print(data)
                    with open("lock_details.json",'w') as lck_details:
                        json.dump(data,lck_details,indent=4) 
                    lck_details.close()  
                    src_fname = db_name+"_Tables.txt"
                    dest_dname = db_name+"_Tables_copy.txt"     
                    shutil.copy(src_fname,dest_dname)   
            lock_details.close()
            
        else:
            lock_dict = {} 
            details = []
            detail_dict = {'lock_acquired': True,'username':username}
            lock_dict['Lock_Details'] = detail_dict
            with open("lock_details.json",'a') as lock_details:                      
                json.dump(lock_dict,lock_details,indent=4)
                src_fname = db_name+"_Tables.txt"
                dest_dname = db_name+"_Tables_copy.txt"     
                shutil.copy(src_fname,dest_dname)   
            lock_details.close()

        for que in range(1,2):
            query = input("enter the {} query in the transaction".format(que))
            query_list.append(query)
        status = input("do you want to commit this transaction?type commit; ")
        for query in query_list:
            self.parse_query(username,db_name,query,logger,fname=db_name+"_Tables_copy.txt")
        if 'commit' in status.lower():
            shutil.copy(db_name+"_Tables_copy.txt",db_name+"_Tables.txt")            
        os.remove(db_name+"_Tables_copy.txt")
        with open("lock_details.json") as lock_details:
            data = json.load(lock_details)
            lock = data['Lock_Details']               
            if lock['lock_acquired'] == True:
                lock['lock_acquired'] = False
                print(data)
                with open("lock_details.json",'w') as lck_details:
                    json.dump(data,lck_details,indent=4)
                lck_details.close()
        lock_details.close()
        self.login_status(username,db_name,logger)

    def parse_createdb(self,username,db_name,logger):
        status = UseDb().create_database(db_name)
        if status:
            query= input("enter query in SQL to process: ")
            words = query.lower().split(' ')
            if words[0] == 'begin':
                self.parse_transactions(username,db_name,logger)
            else:
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
            words = query.lower().split(' ')
            if words[0] == 'begin':
                self.parse_transactions(username,db_name,logger)
            else:
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
    
    def parse_delete(self,username,dbname,query,logger,fname):
        query = query.lower()
        logger.info("parsing delete query, {}".format(query))
        find = re.search('from(.+?)where',query)
        if find:
            table_name = find.group(1).strip().split(' ')
            pattern = re.compile('where(.*)')
            condition = pattern.findall(query)
            status = DeleteOp().delete_data(username,dbname,table_name[0],condition[0].strip(';'),logger,fname)
            if status:
                return
            else:
                self.login_status(username,dbname,logger)

        else:
            pattern = re.compile('from(.*)')
            table_name = pattern.findall(query)
            status = DeleteOp().delete_data(username,dbname,table_name[0].strip(';'),logger=logger,fname=fname)
            if status:
                return
            else:
                self.login_status(username,dbname,logger)
            
    def parse_drop(self,username,dbname,query,logger,fname):
        query = query.lower()
        logger.info("parsing drop query, {}".format(query))
        pattern = re.compile('table(.*)')
        table_name = pattern.findall(query)
        status = DropOp().drop_table(username,dbname,table_name[0].strip(';'),logger,fname)
        if status:
            return
        else:
            self.login_status(username,dbname,logger)
