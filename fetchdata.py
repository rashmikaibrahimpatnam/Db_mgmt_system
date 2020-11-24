import json
import pandas as pd
import re
from tabulate import tabulate

class FindData():
    def fetch_data(self,uname,table_name,columns,condition=None):
        with open(uname+"_tables.txt") as user_tables:
            data = json.load(user_tables)
            tables = data['Tables']
            print(tables)
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    table_data = table['Table_columns']
                    for col in columns:
                        if col == '*':
                            for data in table_data:
                                if condition != None:
                                    g_op = re.search(">",condition)
                                    l_op = re.search("<",condition)
                                    e_op = re.search("=",condition)
                                    if g_op:
                                        lst = condition.split('>')
                                        if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) > int(lst[1].lower().strip()):
                                            datafrm = pd.DataFrame(data,index=[0])
                                            print(datafrm)
                                            '''for key in data:
                                                print(data[key])
                                            print('fetched',data)
                                            #print print print'''
                                    elif l_op:
                                        lst = condition.split('<')
                                        if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) < int(lst[1].lower().strip()):
                                            datafrm = pd.DataFrame(data,index=[0])
                                            print(datafrm)
                                            '''for key in data:
                                                print(data[key])
                                            print('fetched',data)
                                            #place data into the file'''
                                            
                                    elif e_op:
                                        lst = condition.split('=')
                                        if data[lst[0].lower().strip()] == lst[1].lower().strip():
                                            datafrm = pd.DataFrame(data,index=[0])
                                            print(datafrm)
                                            '''for key in data:
                                                print(data[key])
                                            print('fetched',data)
                                            #place data into the file'''
                                               
                                else:
                                    #print everything

                                    datafrm = pd.DataFrame(data,index=[0])
                                    print(datafrm)
                                    
                            '''print(table_data) 
                            for data in table_data:
                                header = data.keys()
                                row = pandas.DataFrame(data.values(), header)                          
                                print(row)'''
                        else:
                            for data in table_data:
                                for key in data:
                                    if col == key:
                                        datafrm = pd.DataFrame(data,index=[0])
                                        print(datafrm)
                                    ''' header = data.keys()
                                        row = pandas.DataFrame(data.values(), header)'''
                    #datafrm = pd.DataFrame(data,index=[0])
                    print(tabulate(pd.DataFrame(table_data, columns=data.keys()),headers = 'keys', tablefmt = 'psql'))
                    print(datafrm) 
           

                                    

                        
