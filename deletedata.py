import re
import json
#from parse import ParseQuery

class DeleteOp():
    def delete_data(self,uname,table_name,condition=None):
        print("delete")
        with open(uname+"_tables.txt",'r') as user_tables:
            data = json.load(user_tables)
            tables = data['Tables']
            print(tables)
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    table_data = table['Table_columns']
                    for data in table_data:
                        if condition == None:
                            for key in data:
                                data[key] = 'null'
                            #place data into the file
                        else:
                            g_op = re.search(">",condition)
                            l_op = re.search("<",condition)
                            e_op = re.search("=",condition)
                            if g_op:
                                lst = condition.split('>')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) < int(lst[1].lower().strip()):
                                    for key in data:
                                        data[key] = 'null'
                                    print('modified',data)
                                    #place data into the file
                                    
                            elif l_op:
                                lst = condition.split('<')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) < int(lst[1].lower().strip()):
                                    for key in data:
                                        data[key] = 'null'
                                    print('modified',data)
                                    #place data into the file
                                    
                            elif e_op:
                                lst = condition.split('=')
                                if data[lst[0].lower().strip()] == lst[1].lower().strip():
                                    for key in data:
                                        data[key] = 'null'
                                    print('modified',data)
                                    #place data into the file
                with open(uname+"_tables.txt",'w') as usr_details:
                    json.dump(data,usr_details,indent=4)                     
        user_tables.close()


