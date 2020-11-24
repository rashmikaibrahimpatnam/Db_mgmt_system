import re


def striptext(text):
    return re.sub(' +', ' ', text.strip())


is_update_query = False
query = "UPDATE Team SET team_name = 'Team 24', team_type = 'AI' WHERE team_name = 'Team 12';"
if re.split(" ", query)[0].lower() == "update":
    is_update_query = True

if is_update_query:
    # do operation
    update_query_set_values = re.split(",",
                                       re.sub("[^A-Za-z0-9=,_]", " ", re.findall(r'set(.*?)where', query.lower())[0]))
    update_query_condition = re.split(",", re.sub("[^A-Za-z0-9=,_]", " ", re.split('where', query.lower())[1]))
    table_name = striptext(re.findall(r'update(.*?)set', query.lower())[0].strip())

    for y in update_query_condition:
        list_condition_update = re.split("=", y)
        key_to_search_for_update_condition = striptext(list_condition_update[0])
        value_update_conditon = striptext(list_condition_update[1])

    for x in update_query_set_values:
        list_key_value_update = re.split("=", x)
        key_to_search = striptext(list_key_value_update[0])
        value_to_update = striptext(list_key_value_update[1])
        # search in dict for condition and perform updates

    print("Update Query Operation")

print('check')
