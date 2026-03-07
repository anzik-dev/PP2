import re
string = input()
words = re.findall("\w+", string)
print(len(words))