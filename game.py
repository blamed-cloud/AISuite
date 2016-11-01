#!/usr/bin/env python



class Game:
	escapes = [":w", ":q", ":wq", ":r"]
	
	def __init__(self, player1, player2, be_quiet = False):
		self.turn = 0
		self.winner = -1
		self.quiet = be_quiet
		self.num_players = 2
		self.players = [None, player1, player2]
		
	def get_turn(self):
		return self.turn
		
	def is_human_turn(self):
		return self.players[self.get_player_num()].is_human()
		
	def current_player(self):
		return self.players[self.get_player_num()]
	
	def handle_escape(self, code):
		if code == ":w":
			print "UnemplementedError: saving"
		elif code == ":wq":
			print "UnemplementedError: saving"
			raise SystemExit
		elif code == ":q":
			raise SystemExit
		elif code == ":r":
			pass
	
	def get_player_num(self):
		return (self.turn % self.num_players) + 1
		
	def __str__(self):
		pass
		
	def load_state_from_string(self, state):
		pass
		
	def __repr__(self):
		return self.__str__()
		
	def opg(self):
		pass
		
	def check_winner(self):
		pass
		
	def is_game_over(self):
		return self.winner != -1
		
	def play(self):
#		if self.history:
#			self.save_state(self.game_file)
		while self.winner == -1:
			self.do_turn()
		if not self.quiet:
			self.opg()
			if self.winner != 0:
				print "PLAYER" + str(self.winner) + " IS THE WINNER!!!"
			else:
				print "IT WAS A DRAW!"
		return self.winner
	
	def get_child_states(self):
		pass
		
	def get_child_moves(self):
		pass
	
	def do_turn(self):
		pass
		
	def make_new_instance(self):
		pass
