import json

def apply_patch(source, patch):
    for key, value in patch.items():
        if value is None:
            if key in source:
                del source[key]
        elif key in source and isinstance(source[key], dict) and isinstance(value, dict):
            apply_patch(source[key], value)
        else:
            source[key] = value
    return source

a1 = json.loads(input())
b1 = json.loads(input())

result = apply_patch(a1, b1)


print(json.dumps(result, sort_keys=True, separators=(',', ':')))
