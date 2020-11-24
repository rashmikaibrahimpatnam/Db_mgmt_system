class CreateDefault:

    def database(self,database_name):
        if len(database_name)== 0 :
            database_name = "assignment_5408"
        else:
            self.database_name = database_name
        flower_bracket_start = '{'
        flower_bracket_end = '}'

        #default structure for dict
        default_json_string = flower_bracket_start+'"Database_name":"'+database_name+'","Tables":[]'+flower_bracket_end
        default_data_type_json_string = flower_bracket_start+'"Database_name":"'+database_name+'","Tables":[]'+flower_bracket_end

        try:
            file1 = open("Tables.txt", "r")
            tables_file = file1.read()
            file1.close()
            file2 = open("Tables_Datatypes.txt", "r")
            tables_datatype_file = file2.read()
            file2.close()
            # write default struct only if empty generally done when user created, check later
            if (len(tables_file) == 0):
                file1 = open("Tables.txt", "w+")
                file1.write(default_json_string)
                file1.close()
            if (len(tables_datatype_file) == 0):
                file2 = open("Tables_Datatypes.txt", "w+")
                file2.write(default_data_type_json_string)
                file2.close()
        except:
            print("schema doesn't exist.. creating new default structure")
            file1 = open("Tables.txt", "w+")
            file1.write(default_json_string)
            file1.close()
            file2 = open("Tables_Datatypes.txt", "w+")
            file2.write(default_data_type_json_string)
            file2.close()

#remove when main is added
crtDbObj = CreateDefault()
crtDbObj.database("")