#!/usr/bin/env python
#mcts.py
import random
import time


class MonteCarloTreeSearch(object):
	def __init__(self, game, simulationPlayerClass, turnTime = 30):
		self.game = game
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
			self.children[childState] = MonteCarloTreeSearch(child, self.simulationClass, self.turnTime)

	def getPoints(self):
		return self.points

	def getVisits(self):
		return self.playouts

	def _selectChildState(self):
		bestScore = 0.0
		bestStates = []
		scalar = math.sqrt(2.0)
		for childState in self.child_states:
			child = self.children[childState]
			exploit = 0
			explore = 0
			if child.getVisits() > 0:
				exploit = child.getPoints()/child.getVisits()
				explore = math.sqrt(2.0 * math.log(self.playouts)/float(child.getVisits()))
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
		self.points += (1/2)*result[0] # should this be 1/numPlayers instead of 1/2 ?
		self.points += result[self.game.get_player_num()]

	def search(self):
		searchStartTime = time.time()
		while (time.time() - searchStartTime < self.turnTime):
			self._selection() #calling _selection on self, no need to update scores

	def _selection(self):
		if self.isLeaf:
			if self.game.is_game_over():
				winner = self.game.winner
				outcome = [0,0,0]
				outcome[winner] = 1
				self._updateScores(outcome)
				return outcome
			else:
				self._enumerateChildren()
				chosenChildState = self._selectChildState()
				result = self.children[chosenChildState]._simulation()
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
		maxPoints = -1
		for childState in self.child_states:
			childPoints = self.children[childState].getPoints()
			if childPoints > maxPoints:
				bestState = childState
				maxPoints = childPoints
		bestMove = self.game.get_child_state2move_dict()[bestState]
		return (bestState, bestMove)


