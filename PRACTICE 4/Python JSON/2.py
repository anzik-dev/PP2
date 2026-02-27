import json

json_string = '{"name": "Anzik", "age": 18}'

data = json.loads(json_string)

print(data)
print(type(data))       
print(data["name"])     