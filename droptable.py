import json
from lockstatus import LockStatus

class DropOp():
    def drop_table(self,username,dbname,table_name,logger,fname):
        check_lock = LockStatus().checklock(username)
        src_fname = dbname+"_Tables.txt"
        dest_dname = dbname+"_Tables_copy.txt"
        if fname == None:            
            filename = src_fname
            status = False
        else:
            filename = dest_dname
            status = True
        with open(filename) as user_tables:
            data = json.load(user_tables)
            tables = data['Tables']
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    #drop table
                    index = tables.index(table)
                    del tables[index]
                    break       
            with open(filename,'w') as usr_details:
                json.dump(data,usr_details,indent=4)  
            usr_details.close()
        user_tables.close()
        return status
