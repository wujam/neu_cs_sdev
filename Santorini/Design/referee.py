"""
The purpose of the Referee is to administer a Santorini game between two players.

A Referee is given two players at initialization, it will keep a Board to keep track of game state
    and a RuleChecker in order to validate moves

The Referee will administer the game state by colling the player whenever it is their
    turn to make a move.
    It will keep track of the stages of the game (worker_placmenets, regular turns, game_over)
    and who's turn it is in order to do this.
"""

class Referee:
    """
    @player1, player2: the two player that the referee will administer games for
    """
    def __init__(self, player1, player2):
        pass

    """
    runs the game from beginning to end through the stages of the game

    After every player action the referee checks the move for validity.
    If the move is not valid then the player who submitted the move loses
    the game and the other player wins.

    It first asks the workers for placements with player1 being the first
    player to act.

    After the worker placement phase is over it asks the players to submit moves
    one at a time.

    After every action in regular turn phase the referee should check if the game
    is over, decide a winner, and end the game
    """
    def run_game(self):
        pass
