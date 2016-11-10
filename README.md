# AISuite

This library serves as a wrapper around a game-engine to provide it with quick access to alpha beta pruning and possibly other AI methods. It provides a base game class that you need to inherit from for compatability with methods called in the player.py and alphabeta.py classes.

## On Your End

To use this library, you need to have at least two things, with an optional third:

* A game engine that deals with necessary game logic and displaying the game
* A heuristic function for the alpha beta pruning algorithm to use.
* A method to determine volatile game states that the AI should search deeper in (optional)

### Game Engine

This part depends largely on what game you are implementing, but in all cases, the game should inherit from the Game class defined in game.py, or you can just use that class itself if that suits your needs better. The method names and comments should provide you with an outline for what you need to do, but not all the methods are truly neccessary, most are just helpful things i've made use of in the past. The methods in the Game class that are used in player.py and alphabeta.py are marked as such by a comment, so you will need to do something about those, but the rest can go unimplimented if you wish.

### Heuristic

A heuristic function is a function that takes a game-state as an argument and returns a number (floats should work, but i've used ints) in a certain range. By default this range is -100 to 100, determined by UPPER_BOUND and LOWER_BOUND in the alphabeta.py file. Positive numbers usually indicate that the first player is winning, negative numbers indicate that the second player is winning, and zero indicates a draw. The heuristic function should return UPPER_BOUND, zero, or LOWER_BOUND if the game-state is that of a game that is finished.

### Volatility

Sometimes it is useful to search deeper in the game tree than you normally would. For example, in chess, you would typically look deeper if the position has any pieces threatening to capture other pieces, to protect against devastating tactics. If you wish, you can write a function that takes a game-state as argurment and returns a bool corresponding to if the game-state is volatile or not. If you do, the alpha beta algorithm will search deeper up to a depth of VOLATILE_DEPTH (as defined in the alphabeta.py file, here negative numbers mean what depth below zero to go to).
