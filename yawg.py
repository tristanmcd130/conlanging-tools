import random, re

class Choice:
	def __init__(self, options, w = []):
		self.options = options
		if w:
			self.weights = w
		else:
			self.weights = [1 / (options.index(x) + 1) for x in options]
	def __call__(self):
		return random.choices(self.options, weights = self.weights, k = 1)
	def __repr__(self):
		return f"Choice({self.options})"

class Option:
	def __init__(self, sequence, p = 0.5):
		self.sequence = sequence
		self.probability = p
	def __call__(self):
		if random.random() <= self.probability:
			return self.sequence
		else:
			return []
	def __repr__(self):
		return f"Option({self.sequence})"

def generate(word_shape):
	queue = word_shape
	while not all([type(x) == str for x in queue]):
		new_queue = []
		for item in queue:
			if type(item) == list:
				for x in item:
					new_queue.append(x)
			elif callable(item):
				for x in item():
					new_queue.append(x)
			elif type(item) == str:
				new_queue.append(item)
			queue = new_queue
	return "".join(queue)

def reject(word, patterns):
	return any([re.search(pattern, word) for pattern in patterns])

def change(word, patterns):
	new_word = word
	for pattern in patterns:
		new_word = re.sub(pattern[0], pattern[1], new_word)
	return new_word
