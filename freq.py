"""
from os import listdir
from re import findall
from ipaparser import IPA
from json import dump

languages = []
phonemes = set()
for filename in sorted(listdir("multilingual-ipa-data/wiktionary/data/ipa")):
	with open("multilingual-ipa-data/wiktionary/data/ipa/" + filename) as file:
		words = findall(r"/[^/]+/|\[[^\]]+\]", file.read())
		print(f"{filename} ({len(words)})")
		languages.append({})
		for word in words:
			for phoneme in [str(symbol) for symbol in IPA(word) if symbol.is_sound()]:
				phonemes.add(phoneme)
				if phoneme in languages[-1]:
					languages[-1][phoneme] += 1
				else:
					languages[-1][phoneme] = 1

frequencies = {}
for phoneme in phonemes:
	frequencies[phoneme] = [0, 0]
	for language in languages:
		if phoneme in language:
			frequencies[phoneme][0] += language[phoneme]
			frequencies[phoneme][1] += sum(language.values())
	frequencies[phoneme] = frequencies[phoneme][0] / frequencies[phoneme][1]

with open("frequencies2", "w") as file:
	dump(dict(sorted(frequencies.items(), key = lambda x: -x[1])), file, ensure_ascii = False, indent = 4)
exit()
#"""

from json import load

with open("/home/tristan/Documents/Conlangs/frequencies2") as file:
	frequencies = load(file)

consonants = input("C: ").split(" ")
vowels = input("V: ").split(" ")
try:
	print(" ".join(sorted(consonants, key = lambda x: -frequencies[x])))
except KeyError:
	print(f"Not in C: {[c for c in consonants if c not in frequencies]}")
	print(" ".join(sorted([c for c in consonants if c in frequencies], key = lambda x: -frequencies[x])))
try:
	print(" ".join(sorted(vowels, key = lambda x: -frequencies[x])))
except KeyError:
	print(f"Not in V: {[v for v in vowels if v not in frequencies]}")
	print(" ".join(sorted([v for v in vowels if v in frequencies], key = lambda x: -frequencies[x])))