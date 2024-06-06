import random, re

class Choice:
	def __init__(self, choices, weights = None):
		self.choices = choices
		if type(weights) == list:
			assert len(weights) == len(choices), "weights must be the same length as choices"
			self.weights = weights
		else:
			self.weights = [1/x for x in range(1, len(choices) + 1)]
	def __call__(self):
		return random.choices(self.choices, self.weights)[0]

class Option:
	def __init__(self, value, prob = 1/2):
		self.value = value
		assert 0 <= prob <= 1, "prob must be within [0, 1]"
		self.prob = prob
	def __call__(self):
		if random.random() < self.prob:
			return self.value
		return ""

def evaluate(word_shape):
	if type(word_shape) in [Choice, Option]:
		return evaluate(word_shape())
	if type(word_shape) == list:
		return "".join([evaluate(x) for x in word_shape])
	if type(word_shape) == str:
		return word_shape
	raise ValueError(f"Invalid word shape {word_shape}")

def generate(word_shape, num_words = 100, rejections = [], filters = {}):
	words = []
	while len(words) < num_words:
		word = evaluate(word_shape)
		if not any([re.search(r, word) for r in rejections]):
			for (start, end) in filters.items():
				word = re.sub(start, end, word)
			if word not in words:
				words.append(word)
	random.shuffle(words)
	return words