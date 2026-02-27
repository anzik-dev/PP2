import json
my_json = json.loads(input())
number_of_queries = int(input())

def find_value(data, commands):
    current = data
    for com in commands:
        if com == "": continue 
        
        try:
            current = current[com]
        except (IndexError, KeyError, TypeError):
            return "NOT_FOUND"
            
    return json.dumps(current, separators=(',', ':'), ensure_ascii=False)

        
for i in range(number_of_queries):
    queries = input()
    
    clean_query = queries.replace('[', '.').replace(']', '')
    
    commands = clean_query.split(".")
    
    clean_commands = []
    
    for x in commands:
        if x.isdigit():
            x = int(x)
            clean_commands.append(x)
        else:
            clean_commands.append(x)
    result = find_value(my_json, clean_commands)
    print(result)