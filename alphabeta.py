#!/usr/bin/env python
#alphabeta.py
from __future__ import print_function
import sys
import random
import player

#from heuristics import is_volatile
#from heuristics import is_board_won

#from fractoe_board import DEFAULT_GAME_FILE
#from fractoe_board import TEMP_GAME_FILE

UPPER_BOUND = 100
LOWER_BOUND = -100

DEFAULT_DEPTH = 5
VOLATILE_DEPTH = -3

ORDER_NORMAL = 1
ORDER_FREE = 2

def default_volatility_measure(game):
	return False

class ABPruning_Tree_Test(object):
	def __init__(self, game, depth_lim = DEFAULT_DEPTH, A = LOWER_BOUND, B = UPPER_BOUND, heuristic = None, i_am_max = True):
		self.game = game
		self.state = str(self.game)
		self.children = {}
		self.child_moves = {}
		self.best_child = []
		self.alpha = A
		self.beta = B
		self.depth_limit = depth_lim
		self.evaluate = heuristic
		self.is_volatile = default_volatility_measure
		self.value = 0
		self.is_max = i_am_max
		self.have_children = False
		
	def re_init(self, depth, A, B):
		self.depth_limit = depth
		self.alpha = A
		self.beta = B
		self.value = 0
		
	def set_heuristic(self, heuristic):
		self.evaluate = heuristic
		
	def set_volatility_measure(self, vol):
		self.is_volatile = vol
		
	def set_game(self, game):
		self.game = game
		
	def set_children(self):
		# self.child_moves = {}
		# need to get the actual move so that we can return that, not the state.
		self.child_moves = self.game.get_child_state2move_dict()
		self.children = {x:None for x in self.game.get_child_states()}
		
	def get_child_tree_by_state(self, child_state):
		t = self
		if child_state in self.children:
			t = self.children[child_state]
		return t
		
	def is_terminal_node(self):
		return self.game.is_game_over()
		
	def get_best_child_pair(self):
		value = []
		if len(self.best_child)==1:
			value = self.best_child[0]
		else:
			value = random.choice(self.best_child)
		return value
		
	def search(self):
		if (self.depth_limit <= 0 and not self.is_volatile(self.state)) or (self.depth_limit == VOLATILE_DEPTH) or self.is_terminal_node():
			self.value = self.evaluate(self.state)
		else:
			self.set_children()
			if self.is_max:
				self.value = LOWER_BOUND
			else:
				self.value = UPPER_BOUND
			for child_state in self.children:
				if self.children[child_state] == None:
					baby = self.game.make_new_instance()
					baby.load_state_from_string(child_state)
					child = ABPruning_Tree(baby, self.depth_limit-1, self.alpha, self.beta, self.evaluate, not self.is_max)
					child.set_volatility_measure(self.is_volatile)
					self.children[child_state] = child
				else:
					self.children[child_state].re_init(self.depth_limit-1, self.alpha, self.beta)
				child_value = self.children[child_state].search()
				if (self.is_max and child_value > self.value) or (not self.is_max and child_value < self.value):
					self.best_child = [(child_state,self.child_moves[child_state])]
				elif child_value == self.value:
					self.best_child += [(child_state,self.child_moves[child_state])]
				if self.is_max:
					self.value = max(self.value, child_value)
					self.alpha = max(self.alpha, self.value)
				else:
					self.value = min(self.value, child_value)
					self.beta = min(self.beta, self.value)
				if self.beta < self.alpha:
					break
		return self.value

#make more general, consider removing printing, or moving to two classes, one with printing, one without.
#also, work with pickle for game_states and such.
class ABPruning_Tree(object):
	def __init__(self, game, depth_lim = DEFAULT_DEPTH, A = LOWER_BOUND, B = UPPER_BOUND, heuristic = None, i_am_max = True, p_depth = 0):
		self.game = game
		self.state = str(self.game)
		self.children = []
		self.best_child = []
		self.alpha = A
		self.beta = B
		self.depth_limit = depth_lim
		self.evaluate = heuristic
		self.is_volatile = default_volatility_measure
		self.value = 0
		self.is_max = i_am_max
		self.print_depth = p_depth
		
	def set_heuristic(self, heuristic):
		self.evaluate = heuristic
		
	def set_volatility_measure(self, vol):
		self.is_volatile = vol
		
	def set_game(self, game):
		self.game = game
		
	def set_children(self):
		self.children = self.game.get_child_states()
		
	def is_terminal_node(self):
		return self.game.is_game_over()
		
	def get_best_child_pair(self):
		value = []
		if len(self.best_child)==1:
			value = self.best_child[0]
		else:
			size = len(self.best_child)-1
			value = self.best_child[random.randint(0,size)]
		return value
		
	def search(self):
		if (self.depth_limit <= 0 and not self.is_volatile(self.state)) or (self.depth_limit == VOLATILE_DEPTH) or self.is_terminal_node():
			self.value = self.evaluate(self.state)
		else:
			self.set_children()
			if self.depth_limit == DEFAULT_DEPTH:
				if self.print_depth > 0:
					print("TURN", file=sys.stderr)
			indent = "---="
			if self.is_max:
				self.value = LOWER_BOUND
				for child_state in self.children:
					baby = self.game.make_new_instance()
					baby.load_state_from_string(child_state)
					child = ABPruning_Tree(baby, self.depth_limit-1, self.alpha, self.beta, self.evaluate, not self.is_max, self.print_depth)
					child.set_volatility_measure(self.is_volatile)
					child_value = child.search()
					layer = DEFAULT_DEPTH - self.depth_limit	
					if (self.print_depth != 0) and (layer < self.print_depth):
						print(indent * layer + "child is: ", str(child_state), file=sys.stderr)
						print(indent * layer + "child value is: ", str(child_value), file=sys.stderr)
						print(indent * layer + "best value is : ", str(self.value), file=sys.stderr)
					if child_value > self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### new best child found ###", file=sys.stderr)
						self.best_child = [child_state]
					elif child_value == self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### another best child added ###", file=sys.stderr)
						self.best_child += [child_state]
					self.value = max(self.value, child_value)
					self.alpha = max(self.alpha, self.value)
					if self.beta < self.alpha:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "ALPHA cutoff", file=sys.stderr)
						break
			else:
				self.value = UPPER_BOUND
				for child_state in self.children:
					baby = self.game.make_new_instance()
					baby.load_state_from_string(child_state)
					child = ABPruning_Tree(baby, self.depth_limit-1, self.alpha, self.beta, self.evaluate, not self.is_max, self.print_depth)
					child.set_volatility_measure(self.is_volatile)
					child_value = child.search()
					layer = DEFAULT_DEPTH - self.depth_limit
					if (self.print_depth != 0) and (layer < self.print_depth):
						print(indent * layer + "child is: ", str(child_state), file=sys.stderr)
						print(indent * layer + "child value is: ", str(child_value), file=sys.stderr)
						print(indent * layer + "best value is : ", str(self.value), file=sys.stderr)
					if child_value < self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### new best child found ###", file=sys.stderr)
						self.best_child = [child_state]
					elif child_value == self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### another best child added ###", file=sys.stderr)
						self.best_child += [child_state]
					self.value = min(self.value, child_value)
					self.beta = min(self.beta, self.value)
					if self.beta < self.alpha:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "BETA cutoff", file=sys.stderr)
						break
			if self.depth_limit == DEFAULT_DEPTH:
				if self.print_depth > 0:
					print("END TURN\n", file=sys.stderr)
		return self.value
	

