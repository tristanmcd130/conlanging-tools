"""
from os import listdir
from re import findall
from ipaparser import IPA
from json import dump

languages = []
phonemes = []
for filename in sorted(listdir("multilingual-ipa-data/wiktionary/data/ipa")):
	print(filename)
	languages.append({})
	with open("multilingual-ipa-data/wiktionary/data/ipa/" + filename) as file:
		for word in findall(r"/[^/]+/|\[[^\]]+\]", file.read()):
			for phoneme in [str(symbol) for symbol in IPA(word) if symbol.is_sound()]:
				if phoneme not in phonemes:
					phonemes.append(phoneme)
				if phoneme in languages[-1]:
					languages[-1][phoneme] += 1
				else:
					languages[-1][phoneme] = 1

frequencies = {}
for phoneme in phonemes:
	frequencies[phoneme] = 0
	for language in languages:
		if phoneme in language:
			frequencies[phoneme] += language[phoneme] / sum(language.values())
	frequencies[phoneme] /= len([l for l in languages if phoneme in l])

with open("frequencies", "w") as file:
	dump(dict(sorted(frequencies.items(), key = lambda x: -x[1])), file, ensure_ascii = False, indent = 4)
exit()
#"""

from json import load

with open("/home/tristan/Documents/Conlangs/frequencies2") as file:
    frequencies = load(file)

consonants = input("C: ").split(" ")
vowels = input("V: ").split(" ")
print(" ".join(sorted(consonants, key = lambda x: -frequencies[x])))
print(" ".join(sorted(vowels, key = lambda x: -frequencies[x])))