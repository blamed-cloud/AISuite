#!/usr/bin/env python
#genetics.py

import player
import pickle
import random

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
		

class Population(object):
	
	def __init__(self, game_class, generation_file = None, load = False):
		self.game_class = game_class
		self.gen_file = generation_file
		self.gen = None
		self.ancestry = []
		if load:
			self.load_gen_from_file(self.gen_file)
			self.ancestry = [self.gen]
			
		
	def load_gen_from_file(self, gen_file):
		FILE = open(gen_file,'r')
		self.gen = pickle.load(FILE)
		FILE.close()
		
	def create_random_gen(self, example_org, gen_size = 100):
		gen = Generation()
		for i in range(gen_size):
			gen.add_member(example_org.reproduce(example_org,1))	#mutation rate of 1 always mutates; creates random weights.
		return gen
		
	def set_gen(self, gen):
		self.gen = gen
		
	def get_ancestry(self):
		return self.ancestry
		
	def evolve(self, iterations = 10, best_percent = 10):
		for i in range(iterations):
			self.gen.calc_fitness(self.game_class)
			n = int(len(self.gen)/best_percent)
			pairs = []
			while len(pairs) < len(self.gen):
				x = random.randint(0,n-1)
				y = x
				while y == x:
					y = random.randint(0,n-1)
				pairs.append((x,y))
			best_n = self.gen.get_best_n(n)
			new_gen = Generation()
			for p in pairs:
				new_gen.add_member(best_n[p[0]].reproduce(best_n[p[1]]))
			self.ancestry += [new_gen]
			self.gen = new_gen
		
	def export_gen_to_file(self, gen_file):
		FILE = open(gen_file, 'w')
		pickle.dump(self.gen, FILE)
		FILE.close()
		
