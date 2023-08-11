from random import choices, random
from re import findall, sub

class Choice:
	def __init__(self, choices: list, weights: list[int | float] = []):
		self.choices = choices
		if weights:
			assert len(weights) == len(choices)
			self.weights = weights
		else:
			self.weights = [1/x for x in range(1, len(choices) + 1)]
	def choose(self):
		return choices(self.choices, weights = self.weights)[0]

class Option:
	def __init__(self, sequence: list, probability: float = 0.5):
		self.sequence = sequence
		self.probability = probability
	def choose(self):
		if random() < self.probability:
			return self.sequence
		return ""

def generate(shape: list, words: int = 1, rejections: list[str] = [], filters: list[tuple[str, str]] = []) -> list:
	word_list = []
	while len(word_list) < words:
		queue = shape
		while not all([type(x) == str for x in queue]):
			new_queue = []
			for item in queue:
				if type(item) == str:
					new_queue.append(item)
				elif type(item) == list:
					new_queue += item
				elif type(item) in [Choice, Option]:
					new_queue.append(item.choose())
			queue = new_queue
		word = "".join(queue)
		if not any([findall(regex, word) for regex in rejections]) and word not in word_list:
			for (regex, replacement) in filters:
				word = sub(regex, replacement, word)
			word_list.append(word)
	return word_list

c = Choice("n t k m l r s ŋ d b p ᵐb w j ⁿd h ɡ f ᵑɡ".split(" "))
v = Choice("a i u e o".split(" "))
i = [Option(c, 2/3), v]
s = [c, v]
w = [Choice([[i, s], [i], [i, s, s]])]
print("\n".join(generate(w, 100,
	[r"(.+)\1", "ji", "wu"],
	[("[ŋᵑ]", "ng"), ("ᵐ", "m"), ("j", "y"), ("ⁿ", "n"), ("ɡ", "g")]
)))