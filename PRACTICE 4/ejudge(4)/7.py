class Reverse:
    def __init__(self, word):
        self.word = word
    def reverse(self):
        b = ""
        for i in range(len(self.word)-1, -1, -1):
            b += self.word[i]
        print(b)
a = input()
word1 = Reverse(a)
word1.reverse()
            