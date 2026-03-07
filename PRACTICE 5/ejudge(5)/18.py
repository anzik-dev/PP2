import re

text = input()
pattern = input()

escaped_pattern = re.escape(pattern)

matches = re.findall(escaped_pattern, text)

print(len(matches))