#!/usr/bin/env python
#weight_heuristic.py
from alphabeta import UPPER_BOUND
from alphabeta import LOWER_BOUND

class WeightHeuristic(object):
	def __init__(self, weight_m):
		self.weights = weight_m
		
	def __call__(self, game_state):
		value = 0
		state = self.parse(game_state)
		winner = state[0]
		turn = state[1]
		matrix = state[2]
		
		#check if the game is over
		if winner == 1:
			return UPPER_BOUND
		elif winner == 2:
			return LOWER_BOUND
		elif winner == 0:
			return 0
		
		#evaluate based on weights
		for y in range(len(matrix)):
			for x in range(len(matrix[y])):
				token = matrix[y][x]
				value += self.weights[token][y][x]
		
		#respect the bounds
		if value >= UPPER_BOUND:
			value = UPPER_BOUND-1
		elif value <= LOWER_BOUND:
			value = LOWER_BOUND+1
	
		return value
		
	def parse(self, game_state):
		pass
		
	def reproduce(self, other_weights, mutation_rate = .001):
		pass
	
