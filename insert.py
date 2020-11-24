import re


def strip_text(text):
    return re.sub(' +', ' ', text.strip())

flower_bracket_start = '{'
flower_bracket_end = '}'
is_insert_query = False
query = "INSERT INTO Player(player_id,team_id,league_id,player_name,position,age) VALUES(2,2,1,'Robinder Dhillon','Goalie',22);"
#query = "INSERT INTO Player(player_name,position,age) VALUES('Robinder Dhillon','Goalie',22);"

if re.split(" ", query)[0].lower() == "insert":
    is_insert_query = True


table_name = strip_text(re.findall(r'into(.*?)\(', query.lower())[0])
if len(re.findall(r'\((.*?)\)', query.lower()))==1:
    #do direct insertion
    print("ADD DIRECT INSERT with out columns")
elif len(re.findall(r'\((.*?)\)', query.lower()))==2:
    query_tablelevel = re.findall(r'\((.*?)\)', query.lower())
    table_columns = query_tablelevel[0]
else:
    print("ERROR IN QUERY")

query_tablelevel = re.findall(r'\((.*?)\)', query.lower())
table_columns_list = re.split(",", strip_text(query_tablelevel[0]))
table_data_type_list = re.split(",", strip_text(query_tablelevel[1]))
print(is_insert_query)