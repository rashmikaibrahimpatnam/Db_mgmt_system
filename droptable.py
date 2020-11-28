import json

class DropOp():
    def drop_table(self,dbname,table_name,logger):
        with open(dbname+"_Tables.txt") as user_tables:
            data = json.load(user_tables)
            tables = data['Tables']
            print(tables)
            for table in tables:
                if table['Table_name'] == table_name.lstrip():
                    #drop table
                    index = tables.index(table)
                    del tables[index]
                    break       
            with open(dbname+"_Tables.txt",'w') as usr_details:
                json.dump(data,usr_details,indent=4)  
            usr_details.close()
        user_tables.close()
