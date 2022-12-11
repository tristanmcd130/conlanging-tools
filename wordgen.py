from yawg import *

c = Choice("n t k m s l r ʔ b d p ŋ j w h ʃ g z f v tʃ ts ʒ dʒ dz".split(" "))
v = Choice("a i u o e".split(" "))
n = Choice("n m ŋ".split(" "))
i = [Option([c], p = 0.75), v, Option([n], p = 0.25)]
s = [c, v, Option([n], p = 0.25)]
w = [i, Option([s, Option([s])])]

words = []
while len(words) < 100:
	word = generate(w)
	if not reject(word, [r"(.+)\1", r"ji", r"wu", r"[mnŋ][mnŋʔhrl]", r"m[tdkgszʃʒ]", r"n[pbkgrlfv]", r"ŋ[pbtdfvszʃʒ]", r"^ʔ"]):
		word = change(word, [("ʔ", "'"), ("ŋ", "ng"), ("j", "y"), ("tʃ", "c"), ("ʃ", "sh"), ("dʒ", "j"), ("ʒ", "zh")])
		if word not in words:
			words.append(word)

print("\n".join(words))
