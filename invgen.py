import csv, statistics

inventories = {}
phonemes = {}
with open("phoible.csv") as csv_file:
	reader = csv.reader(csv_file)
	next(reader)
	for row in reader:
		if row[3] in inventories:
			if row[6] not in inventories[row[3]]:
				inventories[row[3]].append(row[6])
		else:
			inventories[row[3]] = [row[6]]
		if row[6] in phonemes:
			phonemes[row[6]] += 1
		else:
			phonemes[row[6]] = 1
inventories = inventories.values()

#"""
sizes = [len(i) for i in inventories]
avg_size = statistics.mean(sizes)
std_dev = statistics.stdev(sizes)
inventories = [i for i in inventories if len(i) <= avg_size + 0 * std_dev]
#"""

phonemes = sorted(phonemes.keys(), key = lambda x: phonemes[x])[-200 : ]

def jaccard(a, b):
	return len([item for item in a if item in b]) / len(set(a + b))

def avg_jaccard(a):
	total_jaccard = 0
	for inventory in inventories:
		total_jaccard += jaccard(a, inventory)
	return total_jaccard / len(inventories)

inventory = []
while 1:
	possible_inventories = []
	for phoneme in phonemes:
		if phoneme not in inventory:
			possible_inventories.append(inventory + [phoneme])
	for phoneme in inventory:
		possible_inventories.append([item for item in inventory if item != phoneme])
	new_inventory = sorted(possible_inventories, key = lambda x: avg_jaccard(x))[-1]
	if avg_jaccard(new_inventory) < avg_jaccard(inventory):
		break
	inventory = new_inventory
	print(f"Inventory: {' '.join(inventory)}\nAvg. similarity: {avg_jaccard(inventory)}\n")
