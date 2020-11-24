import json

schema_name = "assignment_5408"
user_privileges_json_string = '{"User_privileges":[{"Username":"Yash","Granted":["CREATE","SELECT","INSERT","UPDATE","DELETE"]},{"Username":"Rashmika","Granted":["CREATE","SELECT","INSERT","UPDATE","DELETE"]}]}'
print('CREATE' in json.loads(user_privileges_json_string)['User_privileges'][0]['Granted'])