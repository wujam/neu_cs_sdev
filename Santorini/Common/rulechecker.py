"""
The purpose of the RuleChecker is to determine if a given move is valid on a given board and if the game is over.
A RuleChecker is initialized with a reference to the Board of a game.
It contains a single method that takes in a move (a worker and a direction, and a direction to build),
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
    determines if a move is valid based on the phase of the game, player turn, and the given move
    @player_number: 1 or 2, the number of the player of the worker that's moving
    @worker_number: 1 or 2, which worker of the player is moving
    @direction_to_move: tuple of an int within [-1, 1] and [-1, 1]. The first number specifies the x direction to move,
                        and the second number represents the y direction to move. Positive x is east, positive y is south.
                        cannot be (0, 0)
    @direction_to_build: tuple of an int within [-1, 1] and [-1, 1]. The numbers specify the direction to build relative
                         to the new position of the worker. If the move is game winning, this should be specified as (0,0).
                         cannot be (0, 0)
    @return: True if the move is valid, False otherwise.

    """
    def is_move_valid(self, player_number: int, worker_number: int, direction_to_move: (int, int), direction_to_build: (int, int)) -> bool:
        if (!self._workers_are_placed()):
            return False 

        # TODO: is a move valid if the game is over?

        # worker move bounds checkin:e bog
        worker_position = self.board.get_worker_position(player_number, worker_number)
        new_worker_position = self._add_pos_and_move(worker_position, direction_to_move)

        if (not self._position_in_bounds(new_worker_position):
            return False

        # height move checking
        old_height = self.board.get_floor_height(*worker_position)
        new_height = self.board.get_floor_height(*new_worker_position)
        if (new_height not in range(0, old_height + 2)):
            return False

        # worker move collision checking
        worker_positions = self.board.get_worker_positions()
        worker_positinos = worker_positions[0] + worker_positions[1]
        if (new_worker_position in worker_positions):
            return False

        # building bounds checking
        build_position = self._add_pos_and_move(new_worker_position, direction_to_build)
        if (not self._position_in_bounds(build_position):
            return False

        # building build checking
        build_building_height = self.board.get_floor_height(*build_position)
        if (build_building_height >= self.board.MAX_BUILDING_HEIGHT):
            return False
        
        # building build collision with worker checking
        if (build_position in worker_positions):
            return False
        return True

    """
    determines if all the workers on the board have been placed
    @return: True if all workers have been placed, False otherwise
    """
    def _workers_are_placed(self) -> bool:
        return None not in self.board.get_workers()

    """
    determines if a position is a valid position within the bounds of the board
    @position: tuple of two ints as (x,y) positions. positive x is east, positive y is south
    @return True if the position is within the board
    """
    def _position_in_bounds(self, position: (int, int)) -> bool:
        return position[0] in range(0, self.board.BOARD_DIMENSION) and\
            position[1] in range(0, self.board.BOARD_DIMENSION)

    """
    adds two tuples together
    @position: tuple of two ints (x,y)
    @move: tuple of two ints (x,y)
    """
    def _add_pos_and_move(self, position: (int., int), move: (int, int)) -> (int, int):
        return tuple(sum(i) for i in zip(position, move))

    """
    checks if the game is over or not based on the plater turn and board
    @player_number: 1 or 2, the number of the player who's turn it is
    @return: True if the game is over, False otherwise
    """
    def is_game_over(self, player_number: int) -> bool:
        pass
