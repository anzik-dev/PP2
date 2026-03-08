data = ["123", 45, 3.14, "67"]

for item in data:
    print(f"Original: {item} ({type(item)})")
    

    if isinstance(item, str) and item.isdigit():
        converted = int(item)
        print(f"Converted to int: {converted} ({type(converted)})")

    elif isinstance(item, (int)):
        converted = float(item)
        print(f"Converted to float: {converted} ({type(converted)})")
    
    elif isinstance(item, (float)):
        converted = int(item)
        print(f"Converted to int: {converted} ({type(converted)})")

print("Type checking and conversion done!")