import re
import json
#import pandas as pd
from tabulate import tabulate

def strip_text(text):
    return re.sub(' +', ' ', text.strip())

username = "Yash"

flower_bracket_start = '{'
flower_bracket_end = '}'

schema_name = "assignment_5408"
#default structure for dict
default_json_string = flower_bracket_start+'"Schema_name":"'+schema_name+'","Tables":[]'+flower_bracket_end
default_data_type_json_string = flower_bracket_start+'"Schema_name":"'+schema_name+'","Tables":[]'+flower_bracket_end

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
        file2 = open("" + username + "_Tables_Datatypes.txt", "w+")
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

is_create_query = False
query = "CREATE TABLE Player (player_id int NOT NULL AUTO_INCREMENT,team_id int DEFAULT NULL,league_id int NOT NULL,player_name varchar(45) NOT NULL,position varchar(45) NOT NULL,age int NOT NULL,PRIMARY KEY (player_id),FOREIGN KEY (team_id) REFERENCES Team (team_id),FOREIGN KEY (league_id) REFERENCES League (league_id));"
#query = "CREATE TABLE Player_duplicate (player_id_duplicate int NOT NULL AUTO_INCREMENT,team_id_duplicate int DEFAULT NULL,league_id_duplicate int NOT NULL,player_name_duplicate varchar(45) NOT NULL,position_duplicate varchar(45) NOT NULL,age_duplicate int NOT NULL,PRIMARY KEY (player_id_duplicate),FOREIGN KEY (team_id_duplicate) REFERENCES Team_duplicate (team_id_duplicate),FOREIGN KEY (league_id_duplicate) REFERENCES League_duplicate (league_id_duplicate));"

if re.split(" ",query)[0].lower() == "create":
    is_create_query=True

table_name = strip_text(re.findall(r'table(.*?)\(',query.lower())[0])
query_tablelevel = re.findall(r'\((.*?)\);',query.lower())[0]
table_columns = re.split(",",strip_text(query_tablelevel))
table_columns_list = []
table_data_type = []

num_of_foreign_keys = len(re.findall(r'foreign key', query.lower()))

primary_key = 'none'
foreign_key = []
foreign_key_table_name = []
foreign_key_column = []

for x in table_columns:
    table_columns_list.append(re.split(" ", x)[0])
    table_data_type.append(re.split(" ", x)[1])
    try:
        primary_key = re.sub("[^A-Za-z0-9_]","",re.split("primary key",x)[1])
    except:
        try:
            foreign_key.append(re.sub("[^A-Za-z0-9_]", "", re.findall(r'foreign key(.*?)references', x)[0]))
        except:
            continue
        try:
            foreign_key_table_name.append(re.split(" ", strip_text(re.sub("[^A-Za-z0-9_]", " ", re.findall(r'references(.*?)\)', x)[0])))[0])
            foreign_key_column.append(re.split(" ", strip_text(re.sub("[^A-Za-z0-9_]", " ", re.findall(r'references(.*?)\)', x)[0])))[1])
        except:
            continue

table_columns_list.remove('primary')
table_data_type.remove('key')

for i in range(0,num_of_foreign_keys) :
    table_columns_list.remove('foreign')
    table_data_type.remove('key')

num_of_table_columns = len(table_columns_list)

table_columns_autoincrement_string = ""
table_columns_autoincrement_string+='"Auto Increment":['
for i in range(0,len(table_columns_list)):
    if "auto_increment" in table_columns[i]:
        table_columns_autoincrement_string +='"Yes"'
    else:
        table_columns_autoincrement_string += '"No"'
    if (i != num_of_table_columns - 1):
        table_columns_autoincrement_string += ','
table_columns_autoincrement_string+= ']'

table_columns_string = ""
for i in range(0,num_of_table_columns):
    if "auto_increment" in table_columns[i]:
        table_columns_string += '"' + table_columns_list[i] + '":1'
    else:
        table_columns_string += '"' + table_columns_list[i] + '":"defaultval"'
    if(i!=num_of_table_columns-1):
        table_columns_string+= ','


table_columns_nullable_string = ""
table_columns_nullable_string+='"Nullable":['
for i in range(0,len(table_columns_list)):
    if "not null" in table_columns[i]:
        table_columns_nullable_string +='"No"'
    else:
        table_columns_nullable_string += '"Yes"'
    if (i != num_of_table_columns - 1):
        table_columns_nullable_string += ','
table_columns_nullable_string+= ']'


table_columns_name_string = ""
table_columns_primary_key_string = ""
table_columns_foreign_key_string = ""
table_columns_name_string+='"Name":['
table_columns_primary_key_string = '"Primary Key":['

for i in range(0,num_of_table_columns):
    table_columns_name_string += '"' + table_columns_list[i] + '"'
    if(primary_key!="none"):
        if(primary_key==table_columns_list[i]):
            table_columns_primary_key_string +='"Yes"'
        else:
            table_columns_primary_key_string += '"No"'
    if(i!=num_of_table_columns-1):
        table_columns_name_string+= ','
        table_columns_primary_key_string+= ','
table_columns_name_string+= ']'
table_columns_primary_key_string+= ']'

table_columns_foreign_key_string = '"Foreign Key":['
table_columns_relationship_string = '"Relationship":['
for i in range(0,num_of_table_columns):
    if(table_columns_list[i] in foreign_key):
        table_columns_foreign_key_string += '"Yes"'
    else:
        table_columns_foreign_key_string += '"No"'
    for j in range(0,num_of_foreign_keys):
        if (foreign_key[j] == table_columns_list[i]):
            table_columns_relationship_string += '"Table Column: '+foreign_key[j] +' in Table:'+table_name+' References Table_column: '+foreign_key_column[j] +' in Table: '+foreign_key_table_name[j]+'"'
            if (j != num_of_foreign_keys - 1):
                table_columns_relationship_string += ','
    if(i!=num_of_table_columns-1):
        table_columns_foreign_key_string+= ','
table_columns_relationship_string+=']'
table_columns_foreign_key_string+= ']'

table_data_type_columns_string = ""
table_data_type_columns_string+='"Data Type":['
num_of_table_data_type_columns = len(table_data_type)
for i in range(0,num_of_table_data_type_columns):
    table_data_type_columns_string += '"' + table_data_type[i] + '"'
    if(i!=num_of_table_columns-1):
        table_data_type_columns_string+= ','
table_data_type_columns_string+= ']'

table_datatype_string = table_columns_name_string +","+table_data_type_columns_string+","+table_columns_nullable_string+","+table_columns_autoincrement_string+","+table_columns_primary_key_string+","+table_columns_foreign_key_string+","+table_columns_relationship_string

final_table_columns_string = flower_bracket_start+table_columns_string+flower_bracket_end
final_table_datatype_string = flower_bracket_start+table_datatype_string+flower_bracket_end
my_table_json_string = flower_bracket_start+'"Table_name":"'+table_name+'","Table_columns":['+final_table_columns_string+ ']'+flower_bracket_end
my_table_data_type_json_string = flower_bracket_start+'"Table_name":"'+table_name+'","Table_columns":['+final_table_datatype_string+ ']'+flower_bracket_end
usertable_dict_obj = json.loads(my_table_json_string)
usertable_datatype_dict_obj = json.loads(my_table_data_type_json_string)

# my_temp_dict = usertable_dict_obj['Tables'][0]['Table_columns'][0]
# table_name_dict =  usertable_dict_obj['Tables'][0]['Table_name']
# latest_obj = usertable_dict_obj['Tables'][0]['Table_columns'].append(my_temp_dict)

file1 = open("Tables.txt", "r")
f1 = file1.read()
file1.close()

f2 = json.loads(f1)
table_exists=False
for k,v in f2.items():
    if(k=="Tables"):
        if(len(v)==0):
            v.append(json.loads(my_table_json_string))
            table_exists = True
            print("Table added!!")
        else:
            for tables in v:
                for k1,v1 in tables.items():
                    if(k1=="Table_name"):
                        if(v1==table_name):
                            table_exists=True
                            print("Error!!! Table already exists")

if(table_exists==False):
    for k, v in f2.items():
        if (k == "Tables"):
            v.append(json.loads(my_table_json_string))
            print("Table added!!")

file3 = open("Tables.txt", "w+")
file3.write(json.dumps(f2))
file3.close()

file4 = open("Tables_Datatypes.txt", "r")
f3 = file4.read()
file4.close()

f4 = json.loads(f3)
table_dt_exists=False
for k,v in f4.items():
    if(k=="Tables"):
        if(len(v)==0):
            v.append(json.loads(my_table_data_type_json_string))
            table_dt_exists = True
            print("Table added!!")
        else:
            for tables in v:
                for k1,v1 in tables.items():
                    if(k1=="Table_name"):
                        if(v1==table_name):
                            table_dt_exists = True
                            print("Error!!! Table already exists")

if(table_exists==False):
    for k, v in f4.items():
        if (k == "Tables"):
            v.append(json.loads(my_table_data_type_json_string))
            print("Table added!!")

file5 = open("Tables_Datatypes.txt", "w+")
file5.write(json.dumps(f4))
file5.close()

#display
file1 = open("Tables.txt", "r")
f1 = file1.read()
file1.close()
file2 = open("Tables_Datatypes.txt", "r")
f2 = file2.read()
file2.close()

usertable_dict_obj = json.loads(f1)
usertable_datatype_dict_obj = json.loads(f2)
# print(json.dumps(usertable_dict_obj, indent = 1))
# print(json.dumps(usertable_datatype_dict_obj, indent = 1))

print("\n")
print("\t\t\t\t\t\t\t\tTable Name: "+usertable_dict_obj['Tables'][0]['Table_name'].capitalize())
val = usertable_dict_obj['Tables'][0]['Table_columns']
#print(tabulate(pd.DataFrame(val, columns=["player_id", "team_id", "league_id", "player_name","position","age"]),headers = 'keys', tablefmt = 'psql'))
#print("\n")

# print("\t\t\t\t\t\t\t\t\t\tTable Name: "+usertable_datatype_dict_obj['Tables'][0]['Table_name'].capitalize())
# val2 = usertable_datatype_dict_obj['Tables'][0]['Table_columns'][0]
# #print(pd.DataFrame(val2, columns=["Name", "Data Type", "Nullable","Auto Increment","Primary Key", "Foreign Key"]))
# print(tabulate(pd.DataFrame(val2, columns=["Name", "Data Type", "Nullable","Auto Increment","Primary Key", "Foreign Key"]),headers = 'keys', tablefmt = 'psql'))
# print("\n")

# val3 = usertable_datatype_dict_obj['Tables'][0]['Table_columns'][0]['Relationship']
# print(val3)
# print("\n")