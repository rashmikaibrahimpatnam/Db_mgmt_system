import re
import json
import shutil
from lockstatus import LockStatus

class DeleteOp():        

    def delete_data(self,username,dbname,table_name,condition=None,logger=None,fname=None):
        check_lock = LockStatus().checklock(username)
        #create db copy
        src_fname = dbname+"_Tables.txt"
        dest_dname = dbname+"_Tables_copy.txt"
        if fname == None:            
            filename = src_fname
            status = False
        else:
            filename = dest_dname
            status = True
        with open(filename,'r') as user_tables:
            jdata = json.load(user_tables)
            tables = jdata['Tables']
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    table_data = table['Table_columns']
                    if condition == None:
                        del table_data[1:]
                        for data in table_data:
                            for key in data:
                                data[key] = 'null'
                        logger.info("data is deleted from the table {}".format(table_name))                        
                    else:
                        for data in table_data:
                            g_op = re.search(">",condition)
                            l_op = re.search("<",condition)
                            e_op = re.search("=",condition)
                            if g_op:
                                lst = condition.split('>')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) > int(lst[1].lower().strip()):
                                    for key in data:
                                        data[key] = 'null'
                                    logger.info("data is deleted from the table {}".format(table_name))
                                    
                            elif l_op:
                                lst = condition.split('<')
                                if data[lst[0].lower().strip()] != 'null' and int(data[lst[0].lower().strip()]) < int(lst[1].lower().strip()):
                                    for key in data:
                                        data[key] = 'null'
                                    logger.info("data is deleted from the table {}".format(table_name))
                                    
                            elif e_op:
                                lst = condition.split('=')
                                res = isinstance(data[lst[0].lower().strip()],int)
                                if res:
                                    given = int(lst[1].lower().strip())
                                else:
                                    given = lst[1].lower().strip()                                
                                if data[lst[0].lower().strip()] == given :
                                    for key in data:
                                        data[key] = 'null'
                                    logger.info("data is deleted from the table {}".format(table_name))
            
            with open(filename,'w') as usr_details:
                json.dump(jdata,usr_details,indent=4) 
            usr_details.close()
        user_tables.close()
        return status


