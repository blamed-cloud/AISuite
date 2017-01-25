#!/usr/bin/env python
#alphabeta.py
from __future__ import print_function
import sys
import random
import player

UPPER_BOUND = 100
LOWER_BOUND = -100

DEFAULT_DEPTH = 5
VOLATILE_DEPTH = -3

ORDER_NORMAL = 1
ORDER_FREE = 2

#function for returning randomly from the shallowest best children
def shallowest_first(best_child_list):
	min_depth = max([tup[2] for tup in best_child_list])	# max because depths start high and go to zero (or negative)
	choices = [tup for tup in best_child_list if tup[2] == min_depth]
	return random.choice(choices)
shallowest_first.sel = max

#function for returning randomly from the deepest best children	
def deepest_first(best_child_list):
	max_depth = min([tup[2] for tup in best_child_list])	# min because depths start high and go to zero (or negative)
	choices = [tup for tup in best_child_list if tup[2] == max_depth]
	return random.choice(choices)
deepest_first.sel = min

#function to simply return randomly from any of the best children, ignoring depth	
def ignore_depth(best_child_list):
	return random.choice(best_child_list)
ignore_depth.sel = lambda x: x[0]

def default_volatility_measure(game):
	return False

class ABPruning_Tree(object):
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
		self.choose_best_child = ignore_depth
		
	def re_init(self, depth, A, B):
		self.depth_limit = depth
		self.alpha = A
		self.beta = B
		self.value = 0
		
	def set_heuristic(self, heuristic):
		self.evaluate = heuristic
		
	def set_child_selector(self, selector):
		self.choose_best_child = selector
		
	def set_volatility_measure(self, vol):
		self.is_volatile = vol
		
	def get_depth(self):
		return self.depth_limit
		
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
			if self.children[child_state] == None:
				child = self.make_child_by_state(child_state)
				self.children[child_state] = child
			t = self.children[child_state]
		else
			t = self.make_child_by_state(child_state)
		return t
		
	def is_terminal_node(self):
		return self.game.is_game_over()
		
	def get_best_child_tuple(self):
		value = []
		if len(self.best_child)==1:
			value = self.best_child[0]
		else:
			value = self.choose_best_child(self.best_child)
		return value
		
	def make_child_by_state(self, child_state):	
		baby = self.game.make_new_instance()
		baby.load_state_from_string(child_state)
		child = ABPruning_Tree(baby, self.depth_limit-1, self.alpha, self.beta, self.evaluate, self.baby.get_player_num() == 1)
		child.set_volatility_measure(self.is_volatile)
		child.set_child_selector(self.choose_best_child)
		return child

	def search(self):
		best_child_depth = 0
		if (self.depth_limit <= 0 and not self.is_volatile(self.state)) or (self.depth_limit == VOLATILE_DEPTH) or self.is_terminal_node():
			self.value = self.evaluate(self.state)
			best_child_depth = self.depth_limit
		else:
			if self.children == {}:
				self.set_children()
			if self.is_max:
				self.value = LOWER_BOUND
			else:
				self.value = UPPER_BOUND
			for child_state in self.children:
				if self.children[child_state] == None:
					child = self.make_child_by_state(child_state)
					self.children[child_state] = child
				else:
					self.children[child_state].re_init(self.depth_limit-1, self.alpha, self.beta)
				search_tup = self.children[child_state].search()
				child_value = search_tup[0]
				child_depth = search_tup[1]
				if (self.is_max and child_value > self.value) or (not self.is_max and child_value < self.value):
					self.best_child = [(child_state,self.child_moves[child_state],child_depth)]
					best_child_depth = child_depth
				elif child_value == self.value:
					self.best_child += [(child_state,self.child_moves[child_state],child_depth)]
					best_child_depth = self.choose_best_child.sel([best_child_depth, child_depth])
				if self.is_max:
					self.value = max(self.value, child_value)
					self.alpha = max(self.alpha, self.value)
				else:
					self.value = min(self.value, child_value)
					self.beta = min(self.beta, self.value)
				if self.beta < self.alpha:
					break
		return (self.value, best_child_depth)


