from random import random
from math import exp, log

def anneal(init_state, init_temp):
	state = init_state
	best_energy = state.energy()
	best_state = state
	step = 1
	try:
		while True:
			new_state = state.neighbor()
			if probability(state.energy(), e := new_state.energy(), t := temperature(init_temp, step)) >= random():
				state = new_state
				if e < best_energy:
					best_energy = e
					best_state = state
				print(f"Step: {step}\nTemperature: {t}\nState: {state}\nEnergy: {e}\n")
			step += 1
	except KeyboardInterrupt:
		return best_state

def probability(energy, new_energy, temperature):
	if new_energy <= energy:
		return 1
	return exp((energy - new_energy) / temperature)

def temperature(init_temp, step):
	return init_temp / log(step + 1e-15)