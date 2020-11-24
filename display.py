import json
import pandas as pd
from tabulate import tabulate
from fileops import FileOps

class Display:

    # add methods as required seperately donot modify these
    def print_tables(self,dict_object):
        # add methods as required seperately donot modify these
        print("\n======Tables=======")
        for i in dict_object['Tables']:
            print("\n")
            print("Table Name: " + i['Table_name'].capitalize())
            tables_headers = list(i['Table_columns'][0].keys())
            val = i['Table_columns']
            print(tabulate(pd.DataFrame(val, columns=tables_headers),
                           headers='keys', tablefmt='psql'))
            print("\n")

    def print_datadictionary(self,datatype_dict_object):
        # add methods as required seperately donot modify these
        print("\n======Data Dictionary=======")
        for i in datatype_dict_object['Tables']:
            print("\n")
            print("Table Name: " + i['Table_name'].capitalize())
            tables_headers = list(i['Table_columns'][0].keys())
            tables_headers.remove("Relationship")
            val = i['Table_columns'][0]
            print(tabulate(pd.DataFrame(val, columns=tables_headers),
                           headers='keys', tablefmt='psql'))
            print("\n")

    def print_relationships(self,datatype_dict_object):
        # add methods as required seperately donot modify these
        print("\n======Relationships between Tables=======")
        for i in datatype_dict_object['Tables']:
            print("\n")
            print("Table Name: " + i['Table_name'].capitalize())
            tables_headers = ["Relationship"]
            val = i['Table_columns'][0]
            print(tabulate(pd.DataFrame(val, columns=tables_headers),
                           headers='keys', tablefmt='psql'))
            print("\n")

#call from different method where queries are parsed
fileopobj = FileOps()
f1 = fileopobj.filereader("Tables.txt")
f2 = fileopobj.filereader("Tables_Datatypes.txt")
usertable_dict_obj = json.loads(f1)
usertable_datatype_dict_obj = json.loads(f2)

# print(json.dumps(usertable_dict_obj, indent = 1))
# print(json.dumps(usertable_datatype_dict_obj, indent = 1))

displayObj=Display()

displayObj.print_tables(usertable_dict_obj)

displayObj.print_datadictionary(usertable_datatype_dict_obj)

displayObj.print_relationships(usertable_datatype_dict_obj)
