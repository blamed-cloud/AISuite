#!/usr/bin/env python
#genetics.py

import player
import pickle
import random

class Generation(object):
	
	def __init__(self, game_class):
		self.generation = []
		self.fit_calced = False
		self.game_class = game_class
		
	def add_member(self, organism):
		self.generation.append(organism)
		self.fit_calced = False
		
	def __len__(self):
		return len(self.generation)
		
	def calc_fitness(self, num_games_first = 5, depth = 3, quiet = False):
		org_num = 0
		for org in self.generation:
			org_num += 1
			if not quiet:
				print "organism number: " + str(org_num)
			org_player = player.AI_ABPruning(org, depth_lim = depth)
			r_player = player.Random_TreeAI(depth)
			for x in range(num_games_first):
				if not quiet:
					print "    Game num: " + str(x)
				g_first = self.game_class(org_player, r_player, be_quiet = True)
				g_second = self.game_class(r_player, org_player, be_quiet = True)
				w_f = g_first.play() == 1
				org_player.reset()
				r_player.reset()
				w_s = g_second.play() == 2
				org_player.reset()
				r_player.reset()
				org.record_game(w_f)
				org.record_game(w_s)
			if not quiet:
				print "    Fitness: " + str(org.get_fitness())
		self.fit_calced = True
				
	def report_fitness(self):
		if not self.fit_calced:
			self.calc_fitness()
		org_num = 0
		for org in self.generation:
			org_num += 1
			print "organism" + str(org_num() + ": " + str(org.get_fitness())
	
	def fit_sort(self):
		if not self.fit_calced:
			self.calc_fitness()
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
		gen = Generation(self.game_class)
		for i in range(gen_size):
			gen.add_member(example_org.reproduce(example_org,1))	#mutation rate of 1 always mutates; creates random weights.
		return gen
		
	def load_random_gen(self, example_org, gen_size = 100):
		self.set_gen(self.create_random_gen(example_org, gen_size))
		
	def set_gen(self, gen):
		self.gen = gen
		
	def get_ancestry(self):
		return self.ancestry
		
	def evolve(self, iterations = 10, best_percent = 10, num_games_first = 5, depth = 3, quiet = False):
		for i in range(iterations):
			if not quiet:
				print "Iteration " + str(i)
			self.gen.calc_fitness(self.game_class, num_games_first, depth, quiet)
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
		
