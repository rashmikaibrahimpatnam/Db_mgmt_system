import re
import json
import pandas as pd

def strip_text(text):
    return re.sub(' +', ' ', text.strip())

is_create_query = False
query = "CREATE TABLE Player (player_id int NOT NULL AUTO_INCREMENT,team_id int DEFAULT NULL,league_id int NOT NULL,player_name varchar(45) NOT NULL,position varchar(45) NOT NULL,age int NOT NULL,PRIMARY KEY (player_id),FOREIGN KEY (team_id) REFERENCES Team (team_id),FOREIGN KEY (league_id) REFERENCES League (league_id));"
if re.split(" ",query)[0].lower() == "create":
    is_create_query=True

username = "Yash"
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
table_columns_string = ""
for i in range(0,num_of_table_columns):
    table_columns_string += '"' + table_columns_list[i] + '":"null"'
    if(i!=num_of_table_columns-1):
        table_columns_string+= ','

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


table_datatype_string = table_columns_name_string +","+table_data_type_columns_string+","+table_columns_primary_key_string+","+table_columns_foreign_key_string+","+table_columns_relationship_string

flower_bracket_start = '{'
flower_bracket_end = '}'
final_table_columns_string = flower_bracket_start+table_columns_string+flower_bracket_end
final_table_datatype_string = flower_bracket_start+table_datatype_string+flower_bracket_end
my_table_json_string = flower_bracket_start+'"User":"'+username+'","Tables":['+flower_bracket_start+'"Table_name":"'+table_name+'","Table_columns":['+final_table_columns_string+ ']'+flower_bracket_end+']'+flower_bracket_end
my_table_data_type_json_string = flower_bracket_start+'"User":"'+username+'","Tables":['+flower_bracket_start+'"Table_name":"'+table_name+'","Table_columns":['+final_table_datatype_string+ ']'+flower_bracket_end+']'+flower_bracket_end
usertable_dict_obj = json.loads(my_table_json_string)
usertable_datatype_dict_obj = json.loads(my_table_data_type_json_string)

# my_temp_dict = usertable_dict_obj['Tables'][0]['Table_columns'][0]
# table_name_dict =  usertable_dict_obj['Tables'][0]['Table_name']
# latest_obj = usertable_dict_obj['Tables'][0]['Table_columns'].append(my_temp_dict)

file1 = open(""+username+"_Tables.txt", "a")
file1.write(json.dumps(usertable_dict_obj))
file1.close()

#createdatatype and primary key foriegn key
file2 = open(""+username+"_Tables_Datatypes.txt", "a")
file2.write(json.dumps(usertable_datatype_dict_obj))
file2.close()

print(json.dumps(usertable_dict_obj, indent = 1))
print(json.dumps(usertable_datatype_dict_obj, indent = 1))

print("\n")
val = usertable_dict_obj['Tables'][0]['Table_columns']
print(pd.DataFrame(val, columns=["player_id", "team_id", "league_id", "player_name","position","age"]))
print("\n")

val2 = usertable_datatype_dict_obj['Tables'][0]['Table_columns'][0]
print(pd.DataFrame(val2, columns=["Name", "Data Type", "Primary Key", "Foreign Key"]))
print("\n")

val3 = usertable_datatype_dict_obj['Tables'][0]['Table_columns'][0]['Relationship']
print(val3)
print("\n")