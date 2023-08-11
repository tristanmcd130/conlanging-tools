import csv, random, simanneal

class Inventory:
	def __init__(self, p):
		self.phonemes = p
	def energy(self):
		return (sum([1 - self.jaccard(inventory) for inventory in inventories]) / len(inventories))
	def neighbor(self):
		if random.random() < 0.5:
			return Inventory(self.phonemes + [random.choice([phoneme for phoneme in phonemes if phoneme not in self.phonemes])])
		return Inventory(random.sample(self.phonemes, len(self.phonemes) - 1))
	def jaccard(self, other):
		return len([x for x in self.phonemes if x in other.phonemes]) / len(set(self.phonemes + other.phonemes))
	def __str__(self):
		return str(sorted(self.phonemes))

inventories = {}
phonemes = []
with open("phoible.csv") as csv_file:
	reader = csv.reader(csv_file)
	next(reader)
	for row in reader:
		if row[3] not in inventories:
			inventories[row[3]] = []
		if row[6] not in inventories[row[3]]:
			inventories[row[3]].append(row[6])
		if row[6] not in phonemes:
			phonemes.append(row[6])
avg = sorted([len(i) for i in inventories.values()])
avg = avg[round(len(avg) * 0.5)]
inventories = [Inventory(i) for i in inventories.values() if len(i) <= avg]
print(simanneal.anneal(random.choice(inventories), 1e-2))