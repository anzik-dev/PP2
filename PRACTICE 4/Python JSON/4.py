import json

data = {
    "name": "Anzik",
    "age": 18,
    "skills": ["Python", "Django"]
}

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)