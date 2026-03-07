import re
a = input()
pattern = re.compile(r"^[0-9]+$")
match = pattern.search(a)
if match:
    print("Match")
else:
    print("No match")