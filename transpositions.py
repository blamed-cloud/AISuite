#!/usr/bin/env python
#alphabeta.py

#class to essentially memoize the search function of ABPruning_Tree.
#basically list of tuples of (Transposition_State, depth, alpha, beta, value, best_child_depth)
#implement __contains__ function.

class Transposition_Key(object):
	def __init__(self, _t_state, _depth, _alpha, _beta, _max):
		self.t_state = _t_state
		self.depth = _depth
		self.alpha = _alpha
		self.beta = _beta
		self.max = _max


class Transposition_Manager(object):
	def __init__(self, strictness = 1):
		self.searches = {}	# self.searches : (t_state, max) -> [depth, alpha, beta]
		self.results = {}	# self.results : (t_state, max) -> (value, best_depth)
		self.search_strictness = 1
		if strictness in [0,1,2,3]:
			self.search_strictness = strictness
			# search_stricness	discretion
			# 0			t_state, max
			# 1			t_state, max, depth
			# 2			t_state, max, depth, alpha or beta
			# 3			t_state, max, depth, alpha, beta
	
	
	#returns False if:
	#	search has never been done
	#	or, the new search parameters are more likely to give a better result.
	#returns True if:
	#	search has been done before
	#	and, the previously recorded search is more likely to be accurate.	
	#
	#in general,
	#	bigger depth means better search.
	#	smaller alphas means better search.
	#	bigger betas means better search.
	def __contains__(self, key):
		if not isinstance(key, Transposition_Key):
			raise TypeError
		k = (key.t_state, key.max)
		is_in = (k in self.searches)
		if is_in:
			search_params = self.searches[k]
		is_valid = False
		if is_in and self.search_strictness == 0:
			is_valid = True
		if is_in and self.search_strictness == 1:
			if search_params[0] >= key.depth:	#if the search we have on record is from higher up.
				is_valid = True
		if is_in and self.search_strictness == 2:
			if search_params[0] >= key.depth:
				if search_params[1] <= key.alpha or search_params[2] >= key.beta:
					is_valid = True
		if is_in and self.search_strictness == 3:
			if search_params[0] >= key.depth:
				if search_params[1] <= key.alpha and search_params[2] >= key.beta:
					is_valid = True					
		return is_valid
		
		
	def __getitem__(self, key):
		if key in self:
			return self.results[(key.t_state, key.max)]
		else:
			raise KeyError
		
		
	def get_search_params(self, key):
		if key in self:
			return self.searches[(key.t_state, key.max)]
		else:
			raise KeyError	
		
		
	def __setitem__(self, key, value):
		if not isinstance(key, Transposition_Key):
			raise TypeError
		if len(value) != 2:
			raise ValueError
		else:
			if not isinstance(value[0], int) or not isinstance(value[1], int):
				raise ValueError
		self.searches[(key.t_state, key.max)] = [key.depth, key.alpha, key.beta]
		self.results[(key.t_state, key.max)] = value
		
		
	def __len__(self):
		return len(self.results)
		
		
	def get_strictness(self):
		return self.search_strictness
		

