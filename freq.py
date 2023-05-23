"""
from os import listdir
from re import findall
from ipaparser import IPA

phonemes = []
languages = []
files = listdir("multilingual-ipa-data/wiktionary/data/ipa/")
files_read = 1
for filename in files:
	print(f"{files_read}/{len(files)} ({filename})")
	languages.append([])
	with open(f"multilingual-ipa-data/wiktionary/data/ipa/{filename}", "r") as f:
		content = f.read()
		words = findall(r"(\/.+\/)", content) + findall(r"(\[.+\])", content)
		for word in words:
			for symbol in IPA(word):
				if symbol.is_sound():
					if str(symbol) not in phonemes:
						phonemes.append(str(symbol))
					languages[-1].append(str(symbol))
	files_read += 1

frequencies = {}
for phoneme in phonemes:
	avg_use_per_lang = [lang.count(phoneme) / len(lang) for lang in languages]
	frequencies[phoneme] = sum(avg_use_per_lang) / len(languages)

frequencies = sorted(frequencies.items(), key = lambda x: x[1])
#with open("frequencies", "w") as f:
#	f.write(str(frequencies))
print(frequencies)
exit()
#"""

with open("frequencies", "r") as f:
	occurrences = [x[0] for x in eval(f.read())]

consonants = input("C: ").split(" ")
vowels = input("V: ").split(" ")
print(f"Not found: {[p for p in consonants if p not in occurrences] + [p for p in vowels if p not in occurrences]}")
print(" ".join(sorted([p for p in consonants if p in occurrences], key = lambda x: -occurrences.index(x))))
print(" ".join(sorted([p for p in vowels if p in occurrences], key = lambda x: -occurrences.index(x))))
