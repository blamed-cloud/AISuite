#!/usr/bin/env python
#weight_heuristic.py
import random
from alphabeta import UPPER_BOUND
from alphabeta import LOWER_BOUND

class WeightHeuristic(object):
	def __init__(self, weight_m):
		self.weights = weight_m
		self.wins = 0
		self.losses = 0
		
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
		
	def get_weights(self):
		return self.weights	
	
	def parse(self, game_state):
		pass
		
	def record_game(self, win = False):	# this counts draws as losses, which should be fine since it is across the board.
		if win:
			self.wins += 1
		else:
			self.losses += 1
			
	def get_fitness(self):
		return float(self.wins)/float(self.wins + self.losses)
		
	def reproduce(self, other, mutation_rate = .001):
		child_w = {}
		ow = other.get_weights()
		for token in self.weights:
			matrix = []
			for y in range(len(self.weights[token])):
				row = []
				for x in range(len(self.weights[token])):
					my_w = self.weights[token][y][x]
					other_w = ow[token][y][x]
					new_value = 0
					if my_w*other_w < 0:		# they have opposite signs.
						new_value = random.choice([my_w,other_w])
					elif my_w*other_w > 0:		# they have the same sign.
						new_value = (my_w + other_w)/2
					else:				# at least one is zero.
						if my_w != 0:
							new_value = my_w
						else:
							new_value = other_w
					if random.random() < mutation_rate:	# mutation occured
						new_value = random.randint(LOWER_BOUND,UPPER_BOUND)
					row += [new_value]
				matrix += [row]
			child_w[token] = matrix
		return self.__class__(child_w)
					
					
					
	
