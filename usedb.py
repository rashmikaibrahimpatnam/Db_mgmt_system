import os
import json

class UseDb():
    def use_database(self,dbname):
        file_exists = os.path.isfile(dbname+"_Tables.txt")
        if file_exists:
            return True
        else:
            return False
    def create_database(self,dbname):
        file_exists = os.path.isfile(dbname+"_Tables.txt")
        if file_exists:
            print("db already exists")
            return False
        else:
            #create database/ file structure(redirect to defaut db.py)
            print('im here')
            valdict = {'structure' : 'use other code'}
            with open(dbname+"_Tables.txt",'a') as db_data:
                json.dump(valdict,db_data,indent=4)
            return True