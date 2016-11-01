#!/usr/bin/env python
#player.py
import PythonLibraries.prgm_lib as prgm_lib
import random
import alphabeta
from alphabeta import DEFAULT_DEPTH
from alphabeta import UPPER_BOUND
from alphabeta import LOWER_BOUND

class Player:
	def __init__(self):
		self.human = False
		
	def is_human(self):
		return self.human
		
	def choose_move(self, game)
		pass

		
class Human(Player):
	def __init__(self):
		self.human = True

	def choose_move(self, game)
		return prgm_lib.get_str_escape_codes(game.escapes)
		

class RandomAI(Player):
	def __init__(self):
		self.human = False
		
	def choose_move(self, game):
		moves = game.get_child_moves()
		return random.choice(moves)


class AI_ABPruning(Player):
	def __init__(self, heuristic_func, upper_bound = UPPER_BOUND, lower_bound = LOWER_BOUND, depth_lim = DEFAULT_DEPTH, show_thought_level = 0):
		self.human = False
		self.heuristic = heuristic_func
		self.print_depth = show_thought_level
		self.depth = depth_lim
		self.up = upper_bound
		self.low = lower_bound
		
	def choose_moves(self, game_class, game):
		tree = alphabeta.ABPruning_Tree(game, self.depth, self.low, self.up, self.heuristic, game.get_player_num() == 1, self.print_depth)
		tree.search()
		child = tree.get_best_child()
		return child


