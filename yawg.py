from random import choices, random
from re import findall, sub

class Choice:
	def __init__(self, choices: list, weights: list[float] = []):
		self.choices = choices
		if weights:
			assert len(weights) == len(choices)
			self.weights = weights
		else:
			self.weights = [1 / (x + 1) for x in range(len(choices))]
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

def generate(shape: list, words: int = 1, rejections: list[str] = [], filters: list[tuple[str, str]] = []):
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
		word_list.append("".join(queue))
		if any([findall(regex, word_list[-1]) for regex in rejections]) or word_list[-1] in word_list[ : -1]:
			word_list.pop()
		else:
			for (regex, replacement) in filters:
				word_list[-1] = sub(regex, replacement, word_list[-1])
	return word_list

if __name__ == "__main__":
	c = Choice("n t k m s l r ʔ b d p ŋ j w h g f".split(" "))
	v = Choice("a i u o e".split(" "))
	n = Choice("n. m. ŋ.".split(" "))
	s = [Option([c], 3/4), v, Option([n], 1/4)]
	w = [Choice([[s, s], [s], [s, s, s]])]
	r = [r"(.+)\1", "^ʔ", "ji", "wu", "[iueoa]{3,}", r"m\.[^pbf]", r"n\.[^tds]", r"ŋ\.[^kg]"]
	f = [(r"\.", ""), ("ʔ", "'"), ("ŋ", "ng"), ("j", "y")]
	print("\n".join(generate(w, 100, r, f)))