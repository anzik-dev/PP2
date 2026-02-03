a = int(input())
n = 0
names = []
while a > n:
    name = input()
    names.append(name)
    n+=1
unique_names = list(set(names))
print(len(unique_names))
    