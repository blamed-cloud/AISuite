#!/usr/bin/env python
#game.py
import PythonLibraries.matrix_lib as matrix_lib

class data_square(object):
	def __init__(self, tokens):
		self.data = {}
		self.total = 0
		for t in tokens:
			d = {0:0, 1:0, 2:0}
			self.data[t] = d
		
	def get_prob(self, token, winner):
		num = 1
		if self.data[token][winner] != 0:
			num = self.data[token][winner]
		return num / float(self.total)
		
	def get_total(self):
		return self.total
		
	def get_total_by_token(self,token):
		return sum(self.data[token].values())
		
	def get_total_by_winner(self, winner):
		return sum([x[winner] for x in self.data.values()]) 
		
	def add_game(self, token, winner):
		self.data[token][winner] += 1
		self.total += 1

class Recorder(object):
	def __init__(self, dataFilename, num_rows, num_cols, tokens):
		self.filename = dataFilename
		self.tokens = tokens
		self.rows = num_rows
		self.cols = num_cols
		self.matrix = []
		for y in range(self.rows):
			l = []
			for x in range(self.cols):
				l.append(data_square(self.tokens))
			self.matrix.append(l)
		f = open(self.filename, 'r')
		for line in f:
			self.parse_game(line)
		f.close()
		
	def parse_game(self, game_state):
		grid1 = game_state.split(';')
		winner = int(grid1[-1])
		grid2 = grid1[:self.rows]
		for y in range(self.rows):
			for x in range(self.cols):
				self.matrix[y][x].add_game(grid2[y][x], winner)
		
	def get_data(self, y, x, token, winner):
		return self.matrix[y][x].get_prob(token, winner)
		
	def recorder_heuristic(self, game_state):
		value = 0
		grid1 = game_state.split(';')
		winner = int(grid1[-1])
		grid2 = grid1[:self.rows]
		prob_x = 100.0
		prob_o = 100.0
		prob_d = 100.0
		
		#check for a winner
		if winner == 1:
			return UPPER_BOUND
		elif winner == 2:
			return LOWER_BOUND
		elif winner == 0:
			return 0
		
		#calculate some stuff
		for y in range(self.rows):
			for x in range(self.cols):
				prob_x *= self.get_data(y,x,grid2[y][x],1)
				prob_o *= self.get_data(y,x,grid2[y][x],2)
				prob_d *= self.get_data(y,x,grid2[y][x],0)
				while min(prob_x, prob_o, prob_d) < 10:
					prob_x *= 10
					prob_o *= 10
					prob_d *= 10
				
		#scale
		while max(prob_x, prob_o, prob_d) > 100:
			prob_x /= 10
			prob_o /= 10
			prob_d /= 10
				
		if prob_d > prob_x and prob_d > prob_o:
			value = 0
		else:
			value = int(prob_x - prob_o)
				
		#respect the bounds
		if value >= UPPER_BOUND:
			value = UPPER_BOUND-1
		elif value <= LOWER_BOUND:
			value = LOWER_BOUND+1
	
		return value
				
