import json
import pandas as pd
import re
from tabulate import tabulate

class FindData():
    def fetch_data(self,dbname,table_name,columns,condition=None,logger=None):
        with open(dbname+"_Tables.txt") as user_tables:
            data = json.load(user_tables)
            tables = data['Tables']
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    table_data = table['Table_columns']
                    fetched_data = {}
                    fetched_data[table['Table_name']] = []
                    for col in columns:
                        col = col.strip()                                            
                        for data in table_data:
                            if col == "*" and condition == None:
                                logger.info("data fetched from the table {}".format(table_name))
                                print(tabulate(pd.DataFrame(table_data, columns=data.keys()),headers = 'keys', tablefmt = 'psql'))
                                return
                            elif col != "*" and condition == None:
                                chk = {}
                                for key in data:
                                    if key == col:
                                        chk[key] = data[key]
                                        grouped = fetched_data[table['Table_name']] 
                                        grouped.append(chk)
                                        print(fetched_data)
                            elif condition != None:
                                g_op = re.search(">",condition)
                                l_op = re.search("<",condition)
                                e_op = re.search("=",condition)
                                if g_op:
                                    lst = condition.split('>')
                                    if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) > int(lst[1].lower().strip()):
                                        grouped = fetched_data[table['Table_name']] 
                                        grouped.append(data)
                                        print(fetched_data)
                                elif l_op:
                                    lst = condition.split('<')
                                    if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) < int(lst[1].lower().strip()):
                                        grouped = fetched_data[table['Table_name']] 
                                        grouped.append(data)
                                        print(fetched_data)
                                elif e_op:
                                    lst = condition.split('=')
                                    print(type(data[lst[0].lower().strip()]))
                                    print(type(lst[1].lower().strip()))
                                    res = isinstance(data[lst[0].lower().strip()],int)
                                    if res:
                                        given = int(lst[1].lower().strip())
                                    else:
                                        given = lst[1].lower().strip()
                                    if data[lst[0].lower().strip()] == given:
                                        grouped = fetched_data[table['Table_name']] 
                                        grouped.append(data)
                                        print(fetched_data)
                            
                    if not fetched_data == False and col == "*":
                        logger.info("data fetched from the table {}".format(table_name))
                        print(tabulate(pd.DataFrame(fetched_data[table['Table_name']], columns=data.keys()),headers = 'keys', tablefmt = 'psql'))

                    elif not fetched_data == False and col != "*":
                        logger.info("data fetched from the table {}".format(table_name))
                        df = pd.DataFrame(fetched_data[table['Table_name']], columns=columns)
                        print(df) 
                        print(fetched_data[table['Table_name']])
                        print(tabulate(pd.DataFrame(fetched_data[table['Table_name']], columns=columns),headers = 'keys', tablefmt = 'psql'))

                    
           

                                    

                        
