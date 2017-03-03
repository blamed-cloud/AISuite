#!/usr/bin/env python
#genetics.py

import player

class Generation(object):
	
	def __init__(self):
		self.generation = []
		
	def add_member(self, organism):
		self.generation.append(organism)
		
	def __len__(self):
		return len(self.generation)
		
	def calc_fitness(self, game_class, num_games_first = 5, depth = 3):
		for org in self.generation:
			org_player = player.AI_ABPruning(org, depth_lim = depth)
			r_player = player.RandomAI()
			for x in range(num_games_first):
				g_first = game_class(org_player, r_player, True)
				g_second = game_class(r_player, org_player, True)
				w_f = g_first.play() == 1
				org_player.reset()
				r_player.reset()
				w_s = g_second.play() == 2
				org_player.reset()
				r_player.reset()
				org.record_game(w_f)
				org.record_game(w_s)
				
	def fit_sort(self):
		self.generation = sorted(self.generation, key = lambda x: x.get_fitness())

	def get_best_n(self, n):
		self.fit_sort()
		return self.generation[:n]
		
	
