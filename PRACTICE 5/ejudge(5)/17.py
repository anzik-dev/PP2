import re

text = input()
pattern = r"\d{2}/\d{2}/\d{4}"

l = re.findall(pattern, text)

print(len(l))