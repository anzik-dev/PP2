import json

data = {
    "name": "Anzik",
    "age": 18
}

json_string = json.dumps(data)
print(json_string)

json_string = json.dumps(data, indent=4)
print(json_string)