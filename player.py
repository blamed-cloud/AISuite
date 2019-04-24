#!/usr/bin/env python
#player.py
import PythonLibraries.prgm_lib as prgm_lib
import random
import alphabeta
from alphabeta import DEFAULT_DEPTH
from alphabeta import UPPER_BOUND
from alphabeta import LOWER_BOUND
from mcts import MonteCarloTreeSearch

#base player class
class Player(object):
	def __init__(self):
		self.human = False

	#method to determine if this player is a human
	#is_human : Player -> Bool
	def is_human(self):
		return self.human

	#method to choose a move for the game.
	#choose_move : Player x Game -> Move
	def choose_move(self, game):
		pass

	#method to reset the inner data of the player
	#to be used if you want to play a new game for example
	#reset : Player -> _
	def reset(self):
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

	def reset(self):
		random.seed()


#random opponent with a tree. (hopefully won't lose to depth-move traps)
class Random_TreeAI(Player):
	def __init__(self, depth_lim = DEFAULT_DEPTH, upper_bound = UPPER_BOUND, lower_bound = LOWER_BOUND):
		self.human = False
		self.depth = depth_lim
		self.up = upper_bound
		self.low = lower_bound
		self.tree = None

	def heuristic(self, game_state):
		return random.randint(self.low + 1, self.up - 1)

	def choose_move(self, game):
		if self.tree == None:
			self.tree = alphabeta.ABPruning_Tree(game, self.depth, self.low, self.up, self.heuristic, game.get_player_num() == 1)
		else:
			self.tree = self.tree.get_child_tree_by_state(str(game))
			self.tree.re_init(self.depth, self.low, self.up)
		self.tree.search()
		child_pair = self.tree.get_best_child_tuple()
		self.tree = self.tree.get_child_tree_by_state(child_pair[0])
		return child_pair[1]

	def reset(self):
		random.seed()
		self.tree = None

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
		self.set_sel = False
		self.sel_func = None
		self.depth_sel = None
		self.tree = None

	def set_volatility_func(self, vol):
		self.set_vol = True
		self.vol_func = vol

	def set_child_selector(self, selector, depth_selector):
		self.set_sel = True
		self.sel_func = selector
		self.depth_sel = depth_selector

	def choose_move(self, game):
		if self.tree == None:
			self.tree = alphabeta.ABPruning_Tree(game, self.depth, self.low, self.up, self.heuristic, game.get_player_num() == 1)
			if self.set_vol:
				self.tree.set_volatility_measure(self.vol_func)
			if self.set_sel:
				self.tree.set_child_selector(self.sel_func, self.depth_sel)
		else:
			self.tree = self.tree.get_child_tree_by_state(str(game))
			self.tree.re_init(self.depth, self.low, self.up)
		self.tree.search()
		child_pair = self.tree.get_best_child_tuple()
		self.tree = self.tree.get_child_tree_by_state(child_pair[0])
		return child_pair[1]

	def reset(self):
		self.tree = None


class MCTS_Player(Player):
	def __init__(self, turnTime = 30):
		self.turnTime = turnTime
		self.human = False
		self.mcts = None

	def choose_move(self, game):
		if self.mcts is None:
			self.mcts = MonteCarloTreeSearch(game, RandomAI, self.game.get_player_num(), self.turnTime)
		else:
			self.mcts = self.mcts.childByState(str(game))
		self.mcts.search()

		# print number of visits (out of curiosity)
		if not game.quiet:
			print "Number of Visits: " + str(self.mcts.getVisits())

		stateMovePair = self.mcts.bestMove()
		self.mcts = self.mcts.childByState(stateMovePair[0])
		return stateMovePair[1]

	def reset(self):
		self.mcts = None
