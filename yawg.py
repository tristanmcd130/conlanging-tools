# Yet Another Word Generator

from lark import Lark, Transformer
import random, sys, re

grammar = r"""
?start: ("\n"* rule "\n"*)+
?rule: (category_definition | rejection | filter)? COMMENT?
category_definition: category "=" sequence
sequence: choice+
category: CATEGORY
?choice: weighted_value ("/" weighted_value)* | "[" sequence "]"
?weighted_value: value weight?
weight: ":" NUMBER
?value: category | phoneme | option | sequence
option: "(" sequence ")" probability?
probability: "%" NUMBER
phoneme: PHONEME
rejection: "reject" "=" regex+
regex: REGEX
filter: "filter" "=" regex_change ("," regex_change)*
regex_change: regex "->" regex

CATEGORY: /[A-Z]/
NUMBER: /\d+(\.\d+)?/
PHONEME: /[^\s=\/:\(\)A-Z\->,#%\[\]]+/
REGEX: /[^\s,]+/
COMMENT: /#.+/

%ignore /[ \t]+/
%ignore COMMENT
"""

if len(sys.argv) < 2:
	print("Usage: python yawg.py [file] [number of words to generate]")
	exit()

with open(sys.argv[1], "r") as f:
	text = f.read()

parser = Lark(grammar)
tree = parser.parse(text)
print(tree.pretty())

categories = {}
rejections = []
filters = []

class Choice:
	def __init__(self, choices, weights):
		self.choices = choices
		self.weights = weights
	def choose(self):
		return random.choices(self.choices, weights = self.weights, k = 1)
	def __repr__(self):
		return "(?:" + "|".join([str(x) for x in self.choices]) + ")"

class Option:
	def __init__(self, sequence, probability):
		self.sequence = sequence
		self.probability = probability
	def choose(self):
		return random.random() <= self.probability
	def __repr__(self):
		return "(?:" + "".join([str(x) for x in self.sequence]) + ")?"

class Phoneme:
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return self.value

class Category:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return "".join([str(x) for x in categories[self.name]])

class TreeTransformer(Transformer):
	def phoneme(self, p):
		return Phoneme(p[0].value)
	def weight(self, w):
		return float(w[0].value)
	def weighted_value(self, wv):
		return (wv[0], wv[1])
	def category(self, c):
		return Category(c[0].value)
	def choice(self, c):
		return Choice([x if type(x) != tuple else x[0] for x in c], [1 / (c.index(x) + 1) if type(x) != tuple else x[1] for x in c])
	def sequence(self, s):
		return s
	def probability(self, p):
		return float(p[0].value)
	def option(self, o):
		return Option(o[0], 0.5 if type(o[-1]) != float else o[-1] / 100)
	def regex(self, r):
		return r[0].value
	def filter(self, f):
		global filters
		for rc in f:
			filters.append(rc)
	def rejection(self, r):
		global rejections
		for reg in r:
			new_reg = reg
			for c in categories:
				new_reg = re.sub(c, str(Category(c)), new_reg)
			rejections.append(new_reg)
	def category_definition(self, cd):
		global categories
		categories[cd[0].name] = cd[1]

TreeTransformer().transform(tree)

words = []
if len(sys.argv) > 2:
	num_words = int(sys.argv[2])
else:
	num_words = 100

while len(words) < num_words:
	if "W" not in categories:
		print("Error: No W category defined.")
		exit()
	queue = categories["W"]
	while not all([type(x) == Phoneme for x in queue]):
		#print("QUEUE:", queue)
		new_queue = []
		for element in queue:
			if type(element) == Phoneme:
				new_queue.append(element)
			elif type(element) == Category:
				if element.name not in categories:
					print(f"Error: {element.name} category used but does not exist.")
					exit()
				new_queue += categories[element.name]
			elif type(element) == Choice:
				new_queue.append(element.choose()[0])
			elif type(element) == Option:
				if element.choose():
					new_queue += element.sequence
			elif type(element) == list:
				new_queue += element
			else:
				print(f"Error: Unexpected element of type {type(element)} in queue.")
				exit()
		queue = new_queue
	word = "".join([str(x) for x in queue])
	if not any([re.search(regex, word) for regex in rejections]):
		for replacement in filters:
			word = re.sub(replacement[0], replacement[1], word)
		if word not in words:
			print(word)
			words.append(word)
