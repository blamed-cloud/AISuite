#!/usr/bin/env python
#game.py

#base class for your game_class that you make
class Game:
	#class-specific escape codes for user-input
	escapes = [":w", ":q", ":wq", ":r"]
	
	#defualt constructor, sets up some general variables you might want
	#you can call this with:
	#	super(your_game, self).__init__(player1, player2)
	def __init__(self, player1, player2, be_quiet = False):
		#integer to keep track of the current turn
		self.turn = 0
		
		#integer to keep track of who won or -1 if the game isn't over.
		self.winner = -1
		
		#bool that determines whether to print things to screen.
		self.quiet = be_quiet
		
		#the number of players in the game
		#alpha-beta pruning assumes two players, so having more might be an issue.
		self.num_players = 2
		
		#list for keeping track of the players.
		#index 0 is not used so that each player
		#is at the index of their turn.
		self.players = [None, player1, player2]
		
	#gets the current turn number
	#get_turn : Game -> Int
	def get_turn(self):
		return self.turn
		
	#returns True if the current player is human
	#is_human_turn : Game -> Bool
	def is_human_turn(self):
		return self.players[self.get_player_num()].is_human()
		
	#returns the current player object
	#current_player : Game -> Player
	def current_player(self):
		return self.players[self.get_player_num()]
	
	#handles an escape code that the player may use when doing their turn
	#saving, and evaluating are general things you would have to do.
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
	
	#returns the number of the current player (1 or 2 by default)
	#get_player_num : Game -> Int
	def get_player_num(self):
	### required by player.py ###
		return (self.turn % self.num_players) + 1
		
	#standard python __repr__() function
	#__repr__ : Game -> Str
	def __repr__(self):
		return self.__str__()
		
	#returns True if the game is over
	#is_game_over : Game -> Bool
	def is_game_over(self):
	### required by alphabeta.py ###
		return self.winner != -1
		
	#method to play the game, if you look closely,
	#the do_turn method actually does all the work, have fun.
	#play : Game -> Int
	def play(self):
		while self.winner == -1:
			self.do_turn()
		if not self.quiet:
			self.opg()
			if self.winner != 0:
				print "PLAYER" + str(self.winner) + " IS THE WINNER!!!"
			else:
				print "IT WAS A DRAW!"
		return self.winner
	
	#the remainder of the functions are specific to your implementation.
	#along with these, you should also write a more specific __init__
	#or some other way to create a default game state.
		
	#ideally, this returns a str that is unique to this game's
	#current state, to be used as a way to create games from a
	#string, henceforth known as a Game_State
	#__str__ : Game -> Game_State
	def __str__(self):
	### required by alphabeta.py ###
		pass
			
	#should return a list containing the possible game_states
	#that could result from the current player doing their turn.
	#NOTE: you should use __str__ to create the game_states.
	#get_child_states : Game -> [Game_State]
	def get_child_states(self):
	### required by alphabeta.py ###
		pass
		
	#similar to the previous method, except returns a valid move for your game.
	#its up to you to decide the format for a move that should be used here,
	#and is returned from Player.choose_move
	#get_child_moves : Game -> [Move]
	def get_child_moves(self):
	### required by player.py ###
		pass
	
	#this is where the magic happens.
	#things to do in this method (your needs may vary):
	#	-print the board (possibly only if the current player is human):
	#		human = self.is_human_turn()
	#		if human:
	#			self.opg()
	#	-print stuff for the human
	#		if human:
	#			print <information on playing your turn>
	#	-get the move:
	#		move = self.current_player().choose_move(self)
	#	-check if the move returned is valid, and if it is, update any
	#	 state variables that need to change (such as the turn counter)
	def do_turn(self):
		pass
		
	#method to return an empty class of your type
	#this is done so you can pass whatever arguments your
	#class's __init__ needs
	#make_new_instance : Game -> Game
	def make_new_instance(self):
	### required by alphabeta.py ###
		pass

	#essentially the inverse of the __str__ operation
	#should take a game state, and change the state of the
	#game class to match.
	#load_state_from_string : Game x Game_State -> _
	def load_state_from_string(self, state):
	### required by alphabeta.py ###
		pass
		
	#method for showing the game to the user.
	#short for OutPutGame
	#opg : Game -> _
	def opg(self):
		pass
		
	#Checks if the game is over.
	#stores self.winner as one of {0, 1, 2}
	#depending on if {draw, player1 wins, player2 wins}
	#and returns self.winner
	#check_winner : Game -> Int
	def check_winner(self):
		pass
