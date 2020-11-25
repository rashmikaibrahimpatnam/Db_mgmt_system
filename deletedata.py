import re
import json
#from parse import ParseQuery

class DeleteOp():
    def delete_data(self,dbname,table_name,condition=None,logger=None):
        with open(dbname+"_Tables.txt",'r') as user_tables:
            jdata = json.load(user_tables)
            tables = jdata['Tables']
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    table_data = table['Table_columns']
                    for data in table_data:
                        if condition == None:
                            for key in data:
                                data[key] = 'null'
                            #place data into the file
                            logger.info("data is deleted from the table {}".format(table_name))
                        else:
                            g_op = re.search(">",condition)
                            l_op = re.search("<",condition)
                            e_op = re.search("=",condition)
                            if g_op:
                                lst = condition.split('>')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) > int(lst[1].lower().strip()):
                                    for key in data:
                                        data[key] = 'null'
                                    print('modified',data)
                                    #place data into the file
                                    logger.info("data is deleted from the table {}".format(table_name))
                                    
                            elif l_op:
                                lst = condition.split('<')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) < int(lst[1].lower().strip()):
                                    for key in data:
                                        data[key] = 'null'
                                    print('modified',data)
                                    #place data into the file
                                    logger.info("data is deleted from the table {}".format(table_name))
                                    
                            elif e_op:
                                lst = condition.split('=')
                                res = isinstance(data[lst[0].lower().strip()],int)
                                if res:
                                    given = int(lst[1].lower().strip())
                                else:
                                    given = lst[1].lower().strip()                                
                                if data[lst[0].lower().strip()] == given:
                                    for key in data:
                                        data[key] = 'null'
                                    print('modified',data)
                                    #place data into the file
                                    logger.info("data is deleted from the table {}".format(table_name))
            with open(dbname+"_Tables.txt",'w') as usr_details:
                json.dump(jdata,usr_details,indent=4) 
            usr_details.close()
        user_tables.close()


