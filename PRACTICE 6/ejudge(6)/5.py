n = input()
vowel = "AEIOUaeiou"
if any(i in vowel for i in n):
    print("Yes")
else:
    print("No")
