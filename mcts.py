#!/usr/bin/env python
#mcts.py
import random
import time
import math

class MonteCarloTreeSearch(object):
	def __init__(self, game, simulationPlayerClass, playerNum, turnTime = 30):
		self.game = game
		self.playerNum = playerNum
		self.state = str(game)
		self.child_states = self.game.get_child_states()
		self.children = None
		self.isLeaf = True
		self.turnTime = turnTime
		self.points = 0.0
		self.playouts = 0
		self.simulationClass = simulationPlayerClass

	def _enumerateChildren(self):
		self.children = {}
		for childState in self.child_states:
			child = self.game.make_new_instance()
			child.load_state_from_string(childState)
			self.children[childState] = MonteCarloTreeSearch(child, self.simulationClass, self.playerNum, self.turnTime)

	def getPoints(self):
		return self.points

	def getVisits(self):
		return self.playouts

	def _selectChildState(self):
		bestScore = 0.0
		bestStates = []
		scalar = 1 #math.sqrt(2.0)
		for childState in self.child_states:
			child = self.children[childState]
			exploit = 0
			explore = 0
			if child.getVisits() > 0:
				exploit = child.getPoints()/child.getVisits()
				explore = math.sqrt(2.0 * math.log(self.playouts)/float(child.getVisits()))
			else:
				return childState
			score = exploit + scalar * explore
			if score == bestScore:
				bestStates.append(childState)
			elif score > bestScore:
				bestStates = [childState]
				bestScore = score
		return random.choice(bestStates)

	def _simulation(self, numGames = 1):
		outcomes = [0,0,0]
		for i in range(numGames):
			randomGame = self.game.make_new_instance()
			randomGame.force_quiet()
			randomGame.set_players([None, self.simulationClass(), self.simulationClass()])
			winner = randomGame.play()
			outcomes[winner] += 1
		return outcomes

	def _updateScores(self, result):
		self.playouts += sum(result)
		for i, numGames in enumerate(result[1:]):
			if i == self.playerNum:
				self.points += 100*numGames
			else:
				self.points -= 100*numGames
		# should these be 100/numPlayers instead of 100/2 ?
		# draw takes score toward 0
		if self.points <= 0:
			self.points += 50*result[0]
		else:
			self.points -= 50*result[0]

	def search(self):
		searchStartTime = time.time()
		while (time.time() - searchStartTime < self.turnTime):
			self._selection() #calling _selection on self, no need to update scores

	def _selection(self):
		if self.isLeaf:
			if self.game.is_game_over():
				winner = self.game.winner
				outcome = [0,0,0]
				outcome[winner] = 25
				self._updateScores(outcome)
				return outcome
			else:
				self._enumerateChildren()
				chosenChildState = self._selectChildState()
				result = self.children[chosenChildState]._simulation(3)
				self.children[chosenChildState]._updateScores(result)
				self._updateScores(result)
				self.isLeaf = False
				return result
		else:
			chosenChildState = self._selectChildState()
			result = self.children[chosenChildState]._selection()
			self._updateScores(result)
			return result

	def childByState(self, childState):
		if self.children is not None:
			if childState in self.children:
				return self.children[childState]
		#something probably went wrong...
		raise ValueError("in MonteCarloTreeSearch.childByState, childState did not exist!")

	def bestMove(self):
		bestState = None
		maxPoints = None
		for childState in self.child_states:
			childPoints = self.children[childState].getPoints()
			if maxPoints is None:
				bestState = childState
				maxPoints = childPoints
			elif childPoints > maxPoints:
				bestState = childState
				maxPoints = childPoints
		bestMove = self.game.get_child_state2move_dict()[bestState]
		return (bestState, bestMove)


