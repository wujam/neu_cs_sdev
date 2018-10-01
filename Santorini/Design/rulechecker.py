"""
The purpose of the RuleChecker call is to determine if a given move is valid on a given board.
A RuleChecker is initialized with a reference to the Board of a game.
It contains a single move that takes in a move (a worker and a direction, and a direction to build),
and determines if the move is valid.
Refer to external documentation on what a valid worker move is.
"""
class RuleChecker:
    """
    @board a Board class to validate moves against
    """
    def __init__(self, board):
        self._board = board

    """
    @player_number: 1 or 2, the number of the player of the worker that's moving
    @worker_number: 1 or 2, which worker of the player is moving
    @direction_to_move: tuple of an int within [-1, 1] and [-1, 1]. The first number specifies the x direction to move,
                        and the second number represents the y direction to move. Positive x is east, positive y is south.
    @direction_to_build: tuple of an int within [-1, 1] and [-1, 1]. The numbers specify the direction to build relative
                         to the new position of the worker. If the move is game winning, this should be specified as (0,0).
    @return: a boolean value. True if the move is valid, False otherwise.

    """
    def is_move_valid(self, player_number: int, worker_number: int, direction_to_move: int, direction_to_build: (int, int)) -> bool:
        pass

