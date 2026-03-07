import re
string = input()
x = re.search("cat|dog", string)
if x:
    print("Yes")
else:
    print("No")