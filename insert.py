import re
import json
from fileops import FileOps


class InsertQuery:

    def __init__(self):
        self.fileObj = FileOps()

    def strip_text(self, text):
        return re.sub(' +', ' ', text.strip())

    def insert_row(self, query):

        table_name = re.split(" ", self.strip_text(re.findall(r'into(.*?)\(', query.lower())[0]))[0]

        query_tablelevel = re.findall(r'\((.*?)\)', query.lower())

        if (len(query_tablelevel) == 1):
            table_columns_values_list = re.split(",",
                                                 re.sub("[^A-Za-z0-9_, ]", "", self.strip_text(query_tablelevel[0])))
        else:
            table_columns_headers_list = re.split(",",
                                                  re.sub("[^A-Za-z0-9_, ]", "", self.strip_text(query_tablelevel[0])))
            table_columns_values_list = re.split(",",
                                                 re.sub("[^A-Za-z0-9_, ]", "", self.strip_text(query_tablelevel[1])))

        if len(re.findall(r'\((.*?)\)', query.lower())) == 1:

            # DIRECT INSERT with out columns indication
            print("Inserted rows in Table")
            f1 = json.loads(self.fileObj.filereader("Tables.txt"))
            is_this_table_flag = False
            for k, v in f1.items():
                if (k == "Tables"):
                    for t in v:
                        for k1, v1 in t.items():
                            if (k1 == "Table_name" and v1 == table_name):
                                is_this_table_flag = True
                                continue
                            if (is_this_table_flag):
                                # reset flag once entered
                                is_this_table_flag = False
                                # change default values first i.e first row
                                if (len(v1) == 1 and "defnull" in v1[0].values()):
                                    if (len(v1[0]) == len(table_columns_values_list)):
                                        i = 0
                                        for v1 in v1:
                                            for k2, v2 in v1.items():
                                                if (i < len(table_columns_values_list)):
                                                    v1[k2] = table_columns_values_list[i].capitalize()
                                                    i += 1
                                else:
                                    temp_obj = v1[len(v1) - 1].copy()
                                    v1.append(temp_obj)
                                    i = 0
                                    for k2, v2 in v1[len(v1) - 1].items():
                                        if (i < len(table_columns_values_list)):
                                            v1[len(v1) - 1][k2] = table_columns_values_list[i].capitalize()
                                            i += 1
            self.fileObj.filewriter("Tables.txt", json.dumps(f1))

        elif len(re.findall(r'\((.*?)\)', query.lower())) == 2:
            # insert values in specific columns
            print("Inserted rows in Table")
            f1 = json.loads(self.fileObj.filereader("Tables.txt"))
            f2 = json.loads(self.fileObj.filereader("Tables_Datatypes.txt"))
            is_this_table_flag = False
            auto_increment_list = []
            original_table_col_list = []
            for i in f2['Tables']:
                if(i['Table_name']==table_name):
                    auto_increment_list= i['Table_columns'][0]['Auto Increment']
                    original_table_col_list = i['Table_columns'][0]['Name']

            for k, v in f1.items():
                if (k == "Tables"):
                    for t in v:
                        for k1, v1 in t.items():
                            if (k1 == "Table_name" and v1 == table_name):
                                is_this_table_flag = True
                                continue
                            if (is_this_table_flag):
                                # reset flag once entered
                                is_this_table_flag = False
                                # change default values first i.e first row
                                if (len(v1) == 1 and "defnull" in v1[0].values()):
                                    i = 0
                                    for v1 in v1:
                                        for k2, v2 in v1.items():
                                            if (i < len(table_columns_values_list)):
                                                if (k2 == table_columns_headers_list[i]):
                                                    v1[k2] = table_columns_values_list[i].capitalize()
                                                    i += 1
                                                    continue
                                            if(v2 == "1"):
                                                continue
                                            else:
                                                v1[k2] = "null"
                                else:
                                    temp_obj = v1[len(v1) - 1].copy()
                                    v1.append(temp_obj)
                                    i = 0
                                    j = 0
                                    for k2, v2 in v1[len(v1) - 1].items():
                                        if (i < len(table_columns_headers_list)):
                                            if (k2 == table_columns_headers_list[i]):
                                                v1[len(v1) - 1][k2] = table_columns_values_list[i].capitalize()
                                                i += 1
                                                continue
                                        if(k2 == original_table_col_list[j] and auto_increment_list[j]=="Yes"):
                                            v1[len(v1) - 1][k2] = int(v1[len(v1) - 2][k2])+1
                                            j += 1
                                        else:
                                            v1[len(v1) - 1][k2] = "null"
                                            j += 1

            self.fileObj.filewriter("Tables.txt", json.dumps(f1))

        else:
            print("ERROR IN INSERT QUERY!!!")


# call from different method where queries are parsed
insertObj = InsertQuery()

# query = "INSERT INTO Player(player_id,team_id,league_id,player_name,position,age) VALUES(2,2,1,'Robinder Dhillon','Goalie',22);"
# query = "INSERT INTO Player VALUES(4,1,1,'Sam','Forward',27);"
#query = "INSERT INTO Team(league_id) VALUES(7);"
query = "INSERT INTO Player(player_name,position,age) VALUES('Kethan','Forward',22);"
#query = "INSERT INTO Player(player_name) VALUES('Jordan');"

insertObj.insert_row(query)
is_insert_query = False
if re.split(" ", query)[0].lower() == "insert":
    is_insert_query = True
