'''
category C n t s r k l m d j p h ʔ b g w ŋ ʃ
category V a i e o u
syllable I C?75 V N?25
syllable S C V N?25
word I S? S?
reject (.+)\1 [mnŋ][mnŋʔhrljw] ji wu
filter j>y ʔ>' ŋ>ng ʃ>sh
'''

# Yet Another Word Generator

from sys import argv
from random import randint, choice, choices
from re import search, sub
	
with open(argv[1], "r") as f:
	rules = [line.split(" ") for line in f.read().split("\n")]

categories = {}
syllable_shapes = {}
word_shape = []
rejections = []
filters = {}

for line in rules:
	match line[0]:
		case "category":
			categories[line[1]] = []
			for phoneme in range(2, len(line)):
				categories[line[1]] += [(line[phoneme], 1 / (phoneme - 1))]
		case "uniform":
			categories[line[1]] = []
			for phoneme in range(2, len(line)):
				categories[line[1]] += [(line[phoneme], 1)]
		case "syllable":
			syllable_shapes[line[1]] = line[2 : ]
		case "word":
			word_shape = line[1 : ]
		case "reject":
			rejections = line[1 : ]
		case "filter":
			for regex in line[1 : ]:
				if len(regex.split(">")) > 1:
					filters[regex.split(">")[0]] = regex.split(">")[1]
				else:
					filters[regex.split(">")[0]] = ""
		case "#":
			pass
		case "":
			pass
		case _:
			raise ValueError(line[0] + " is not a valid command.")

if len(argv) > 2:
	words = int(argv[2])
else:
	words = 100

generated_words = []
while words > 0:
	generated_word = []
	
	for syllable in word_shape:
		if "?" in syllable:
			if len(syllable.split("?")[1]):
				probability = int(syllable.split("?")[1])
			else:
				probability = 50
		else:
			probability = 100
			
		if randint(1, 100) <= probability:
			generated_word += syllable_shapes[syllable.split("?")[0]]
	
	for category in range(len(generated_word)):
		if "?" in generated_word[category]:
			if len(syllable.split("?")[1]):
				probability = int(generated_word[category].split("?")[1])
			else:
				probability = 50
		else:
			probability = 100
			
		if randint(1, 100) <= probability:
			generated_word[category] = choices([phoneme[0] for phoneme in categories[generated_word[category].split("?")[0]]], weights = [phoneme[1] for phoneme in categories[generated_word[category].split("?")[0]]], k = 1)[0]
		else:
			generated_word[category] = ""

	generated_word = "".join(generated_word)
	
	if len(rejections):
		if any([search(regex, generated_word) for regex in rejections]):
			continue
	
	if len(filters):
		for regex in filters:
			generated_word = sub(regex, filters[regex], generated_word) 
	
	if generated_word in generated_words:
		continue
	else:
		generated_words += [generated_word]
	
	print(generated_word)
	words -= 1
