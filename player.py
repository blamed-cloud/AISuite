#!/usr/bin/env python
#player.py
import PythonLibraries.prgm_lib as prgm_lib
import random
import alphabeta
from alphabeta import DEFAULT_DEPTH
from alphabeta import UPPER_BOUND
from alphabeta import LOWER_BOUND

#base player class
class Player(object):
	def __init__(self):
		self.human = False

	#method to determine if this player is a human
	#is_human : Player -> Bool		
	def is_human(self):
		return self.human
		
	#method to choose a move for the game.
	#choose_move : Game -> Move
	def choose_move(self, game):
		pass

		
#basic class for a human player
class Human(Player):
	def __init__(self):
		#turns out humans are in fact human
		self.human = True

	#uses terminal user input, may or may not be desirable
	def choose_move(self, game):
		return prgm_lib.get_str_escape_codes(game.escapes)
		

#basic class for a random opponent
class RandomAI(Player):
	def __init__(self):
		self.human = False
		
	#chooses a random move from the possible moves it has this turn
	def choose_move(self, game):
		moves = game.get_child_moves()
		return random.choice(moves)


#class for doing alpha-beta pruning
class AI_ABPruning(Player):
	def __init__(self, heuristic_func, upper_bound = UPPER_BOUND, lower_bound = LOWER_BOUND, depth_lim = DEFAULT_DEPTH, show_thought_level = 0):
		self.human = False
		self.heuristic = heuristic_func
		self.print_depth = show_thought_level
		self.depth = depth_lim
		self.up = upper_bound
		self.low = lower_bound
		self.set_vol = False
		self.vol_func = None
		self.tree = None
		
	def set_volatility_func(self, vol):
		self.set_vol = True
		self.vol_func = vol		
	
	def choose_move(self, game):
		if self.tree == None:
			self.tree = alphabeta.ABPruning_Tree_Test(game, self.depth, self.low, self.up, self.heuristic, game.get_player_num() == 1)
			if self.set_vol:
				self.tree.set_volatility_measure(self.vol_func)
		else:
			self.tree = self.tree.get_child_tree_by_state(str(game))
			self.tree.re_init(self.depth, self.low, self.up)
		self.tree.search()
		child_pair = self.tree.get_best_child_pair()
		self.tree = self.tree.get_child_tree_by_state(child_pair[0])
		return child_pair[1]


