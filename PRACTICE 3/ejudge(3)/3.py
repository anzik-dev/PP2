example = input()
s = ""
l = []
h = []

numbers = {
    "ONE": 1,
    "TWO": 2,
    "THR": 3,
    "FOU": 4,
    "FIV": 5,
    "SIX": 6,
    "SEV": 7,
    "EIG": 8,
    "NIN": 9,
    "ZER": 0
}

reverse_numbers = {v: k for k, v in numbers.items()}


for x in example:
    if x in "+-*":
        l.append(s)
        l.append(x)
        s = ""
    else:
        s += x
l.append(s)


for item in l:
    if item in "+-*":
        h.append(item)
    else:
        num = ""
        for i in range(0, len(item), 3):
            num += str(numbers[item[i:i+3]])
        h.append(num)


result = eval("".join(h))

answer = ""
for digit in str(result):
    answer += reverse_numbers[int(digit)]

print(answer)
