Santorini
=======================================================

Batman and Robin

Changes from existing
---------------------
Many docs were updated because the implementation didn't match the design or the docstrings.

Design
------
In the Design directory is the contents of the board interface for Santorini and our plan 
for designing Santorini.

The first file, `board.py`, is our interface for the Santorini board. In it contains
a class for the Board with methods to place and move Workers, and build a Building on 
the board. The Board class itself has two internal attributes, the `_board` attribute
and the `_workers` attribute. `_board` is a 2-d array of Buildings, all starting with 0
floors. `_workers` is a dictionary mapping wokers to their position on the board. 

The second file, `plan.pdf`, is our design plan for implementing Santorini. In it contains
what we think we'll need to implement the game and the specific classes/methods/etc that
we outlined for using the create the game in our eyes. 

The third file, `player.py`, is our interface for the Santorini player. In it contains a class for
the Player with methods to initialize a player in the game, place a worker, play a turn, and end the game. 

The fourth file, `rulechecker.py`, is our interface for the Santorini RuleChecker. In itcontains a class for the RuleChecker with methods to check all of the defined rules for Santorini. These rules include whether a worker can 
be placed/moved and if a floor can be built in a building. To check these rules, these methods will take in 
a copy of the current board and a worker with a direction. 

The fifth file, `strategy.py` is our interface for the Santorini strategy. In it contains two methods for 
constructing a strategy to play Santorini, plan_turn and plan_placement. Plan_placement returns a valid placement 
for a worker on the board, and plan_turn returns a valid move and build request. 

The sixth file, `referee.py`, is our interface for the Santorini referee. In it contains an AbstractReferee class
that has a list of players in the current game. The class contains two methods, run_game and complete_turn, complete_placement.
run_game will startup the game with the associated players and surpervise turns being played. complete_turn will execute
run_n_games will run n games sequentially and return the player who won the most games.
any turn given by the player's strategy in the game. 

The seventh file `tournament_manager.py`, is our interface for the Santorini Tournament Manager.  It contains a
function that facilitates running a round robin tournament amongst an arbitrary amount of players

Admin
------
The Admin directory contains all the administrative code necessary for the systems to function.

* The directory contains `referee.py`, an implementation of the Referee class
The Referee class is initialized with 2 players, and then the run_game method is called to run the game.
The Referee has methods complete_placement and complete_turn that can be called to make the
Referee get worker placements and get turns from a player, which will be validated and then applied to
the board for their game.
The Referee class also has a method run_n_games, which will run n number of games sequentially, and
then return the player that won the most games.

* The directory also contains `player_guard.py`, a class that serves as a wrapper
for players and guards against players that could be broken or malicious.
It passes up useful errors to callers informing them of how the player broke.


Common
------

In the Common directory are a few of the game pieces we've implemented, in the file `pieces.py`.

`pieces.py` includes:

 * The Board class, which includes two class attributes, the internal
representation of the board and a dictionary of Worker objects associated with their
current board position. The class also includes methods for movement, placement, building, 
getting board attributes, and getting a position on the board. 

 * The Building class, which has a single class attribute for the number
of floors in a building. It also has class methods building a floor onto a building and getting
the current number of floors. 

 * The Worker class, which has class attributes for the player's name its 
associated with and the piece number associated with itself. We also re-define equality and 
hash representations for use later in our logic checking. 

 * The Direction enum, which we define as the different possible directions
a Worker can move on the board. This is used for any movement to ensure that workers can only
ever move in 1-square increments.

`rulechecker.py` includes:

* The RuleChecker class, which includes two methods for checking if you can move and can build.
This will return True/False statements based on the input worker and direction and the current
board state

Player
------

In the player directory is our implementation of our Player interface, along with player strategies. 

`player.py` includes:

* The Player class, which is an implementation of the player in Santorini. The Player
includes its name as a string, a list of Worker objects, and a Strategy object. 
This class also includes four methods, initialize, play_placement, play_turn, and game_over. Over the 
course of a game, the player will initialize itself, play a placement and turns by passing its information
(i.e. workers and current board state) onto the strategy object, which will in turn return a valid turn to 
pass to the referee object to execute.

`place_strat.py` includes:
* The two placement strategies, PlaceStratDiagonal and PlaceStratFar, which are both classes. PlaceStratDiagonal
will return player placement along the diagonal of the game board, and PlaceStratFar will return player placement
the furthest possible away from opposing players. 

`tree_strat.py` includes:
* The TurnStrategy implementation, TreeStrategy. This is a class that has a depth attribute for the look-ahead, 
and methods to get the turn derived by the strategy, find the next turn derived by the strategy, and determine
if the player can survive for a finite amount of turns (get_turn, next_turn, and do_survive, respectively). 


Observer
------

`Observer.py` includes:

* An observer class that plugs into a Referee and prints out game information in JSON format to STDOUT

Tests
-----

In the Tests directory are our unit tests for implemented game pieces. Instructions on how to run these tests
can be found in `testme.md`

Lib
---

In the Lib directory are all of the external methods that we've used to ease development. 

`echo.py` includes

* The function `json_echo`, which we use to parse input to pass onto our test harness. 
