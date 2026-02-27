import json

def find_diff(obj1, obj2, path=""):
    diffs = []
    

    all_keys = sorted(set(obj1.keys()) | set(obj2.keys()))
    
    for key in all_keys:

        current_path = f"{path}.{key}" if path else key
        
        val1 = obj1.get(key, "<missing>")
        val2 = obj2.get(key, "<missing>")
        
        if val1 == val2:
            continue
            

        if isinstance(val1, dict) and isinstance(val2, dict):
            diffs.extend(find_diff(val1, val2, current_path))
        else:

            v1_str = "<missing>" if val1 == "<missing>" else json.dumps(val1, separators=(',', ':'), sort_keys=True)
            v2_str = "<missing>" if val2 == "<missing>" else json.dumps(val2, separators=(',', ':'), sort_keys=True)
            diffs.append(f"{current_path} : {v1_str} -> {v2_str}")
            
    return diffs


a1 = json.loads(input())
b1 = json.loads(input())

result = find_diff(a1, b1)

if not result:
    print("No differences")
else:
    for line in sorted(result):
        print(line)
