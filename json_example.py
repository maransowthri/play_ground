import json


person_dict = {'name': 'Maran', 'Profession' : 'Software Engineer', 'age': 23}
print(json.dumps(person_dict))

json_file = '{"name": "Maran", "Profession": "Software Engineer", "age": 23}'
print(json.loads(json_file))
