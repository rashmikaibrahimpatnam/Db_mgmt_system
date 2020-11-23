import json

flower_bracket_start = '{'
flower_bracket_end = '}'

schema_name = "assignment_5408"
#default structure for dict
user_privileges_json_string = flower_bracket_start+'"User_privileges":[{"Username":"Yash","Granted":["CREATE","SELECT","INSERT","UPDATE","DELETE"]},{"Username":"Rashmika","Granted":["CREATE","SELECT","INSERT","UPDATE","DELETE"]}]'+flower_bracket_end
print('CREATE' in json.loads(user_privileges_json_string)['User_privileges'][0]['Granted'])