import sys

input = sys.stdin.readline  
write = sys.stdout.write

n = int(input())
a = {}

for _ in range(n):
    cmd = input().split()
    if cmd[0] == "set":
        a[cmd[1]] = cmd[2]
    else:  
        key = cmd[1]
        write(a.get(key, f"KE: no key {key} found in the document") + "\n")
