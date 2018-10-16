"""
The purpose of the RuleChecker is to determine if a given move is valid on a given board and if the game is over.
A RuleChecker is initialized with a reference to the Board of a game.
It contains a single method that takes in a move (a worker and a direction, and a direction to build),
and determines if the move is valid.
Refer to external documentation on what a valid worker move is.
"""
class RuleChecker:

    board = None
    DIRECTIONS = [(-1,-1), (0, -1), (1, -1),
                  (-1, 0),          (1,  0),
                  (-1, 1), (0,  1), (1,  1)]

    """
    @board a Board class to validate moves against
    """
    def __init__(self, board):
        self.board = board

    """
    determines if a move is valid based on the phase of the game, player turn, and the given move
    @player_number: 0 or 1, the number of the player of the worker that's moving
    @worker_number: 0 or 1, which worker of the player is moving
    @direction_to_move: tuple of an int within [-1, 1] and [-1, 1]. The first number specifies the x direction to move,
                        and the second number represents the y direction to move. Positive x is east, positive y is south.
                        cannot be (0, 0)
    @return: True if the move is valid, False otherwise.

    """
    def is_move_valid(self, player_number: int, worker_number: int, direction_to_move: (int, int)):
        if (not self._workers_are_placed()):
            return False

        # worker move bounds checking
        worker_position = self.board.get_worker_position(player_number, worker_number)
        new_worker_position = self._add_pos_and_move(worker_position, direction_to_move)

        if (not self._position_in_bounds(new_worker_position)):
            return False

        # height move checking
        old_height = self.board.get_floor_height(*worker_position)
        new_height = self.board.get_floor_height(*new_worker_position)
        if (new_height not in range(0, min(old_height + 2, self.board.MAX_BUILDING_HEIGHT))):
            return False

        # worker move collision checking
        players = self.board.get_worker_positions()
        worker_positions = self._flatten(players)
        if (new_worker_position in worker_positions):
            return False

        return True

    """
    determines if a move is valid based on the phase of the game, player turn, and the given move
    @player_number: 0 or 1, the number of the player of the worker that's moving
    @worker_number: 0 or 1, which worker of the player is moving
    @direction_to_move: tuple of an int within [-1, 1] and [-1, 1]. The first number specifies the x direction to move,
                        and the second number represents the y direction to move. Positive x is east, positive y is south.
                        cannot be (0, 0)
    @direction_to_build: tuple of an int within [-1, 1] and [-1, 1]. The numbers specify the direction to build relative
                         to the new position of the worker. If the move is game winning, this should be specified as (0,0).
                         cannot be (0, 0)
    @return: True if the move is valid, False otherwise.

    """
    def is_move_and_build_valid(self, player_number: int, worker_number: int, direction_to_move: (int, int), direction_to_build: (int, int)) -> bool:
        # check if the move is valid
        if (not self.is_move_valid(player_number, worker_number, direction_to_move)):
            return False

        worker_position = self.board.get_worker_position(player_number, worker_number)
        new_worker_position = self._add_pos_and_move(worker_position, direction_to_move)
        players = self.board.get_worker_positions()

        # building bounds checking
        build_position = self._add_pos_and_move(new_worker_position, direction_to_build)
        if (not self._position_in_bounds(build_position)):
            return False

        # building build checking
        build_building_height = self.board.get_floor_height(*build_position)
        if (build_building_height + 1 > self.board.MAX_BUILDING_HEIGHT):
            return False

        # building build collision with new worker positions
        players[player_number][worker_number] = new_worker_position
        new_worker_positions = self._flatten(players)
        if (build_position in new_worker_positions):
            return False

        return True

    """
    returns a flattened list from a list of lists
    @return flattened list
    """
    def _flatten(self, list_of_lists: [[]]) -> []:
        return [val for sublist in list_of_lists for val in sublist]

    """
    determines if all the workers on the board have been placed
    @return: True if all workers have been placed, False otherwise
    """
    def _workers_are_placed(self) -> bool:
        return not any(None in workers for workers in self.board.get_worker_positions())

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
    @return: tuple of two ints (x,y)
    """
    def _add_pos_and_move(self, position: (int, int), move: (int, int)) -> (int, int):
        return tuple(sum(i) for i in zip(position, move))

    """
    checks if a position can be moved to disregarding height
    @position: tuple of two ints (x, y)
    @workers: a list of all Workers on the board
    @return: True if position is within bounds and no worker occupies it, otherwise false
    """
    def _can_pos_be_moved_to(self, position: (int, int), worker_positions):
        return (self._position_in_bounds(position) and
            position not in worker_positions)

    """
    checks if the game is over or not based on the player turn and board
    @player_number: 0 or 1, the number of the player whose turn it is
    @return: -1 if the game is not over, 0 if the first player won,
             1 if the second player won
    """
    def is_game_over(self, player_number: int) -> bool:
        buildings = self.board.get_building_heights()
        players = self.board.get_worker_positions()

        workers = players[0] + players[1]
        for worker in workers:
            if self.board.get_floor_height(*worker) == 3:
                if worker in players[0]:
                    return 0
                elif worker in players[1]:
                    return 1

        if all(len(self._where_can_worker_move(worker, workers)) == 0 for worker in players[player_number]):
            if worker in players[0]:
                return 1
            elif worker in players[1]:
                return 0

        possible_builds = set()
        for worker in players[player_number]:
            possible_builds.update(self._where_can_worker_build(worker, workers))

        if len(possible_builds) == 0:
            if player_number == 0:
                return 1
            elif player_number == 1:
                return 0
        return -1


    """
    checks where a worker can move
    @worker: tuple of two ints (x, y) within the bounds of the board [0,6)
    @workers: a list of all Workers on the board
    @return: a list of positions that a worker can move to
    """
    def _where_can_worker_move(self, worker, workers):
        worker_height = self.board.get_floor_height(*worker)
        players = self.board.get_worker_positions()
        worker_positions = players[0] + players[1]

        possible_moves = []
        for direction in self.DIRECTIONS:
            new_pos = self._add_pos_and_move(worker, direction)
            if (self._can_pos_be_moved_to(new_pos, workers) and
                self.board.get_floor_height(*new_pos) - worker_height <= 1):
                possible_moves.append(new_pos)
        return possible_moves

    """
    checks where a worker can build
    @worker: tuple of two ints (x, y) within the bounds of the board [0,6)
    @workers: a list of all Workers on the board
    @return: a list of positions that a worker can move to
    """
    def _where_can_worker_build(self, worker, workers):
        possible_moves = self._where_can_worker_move(worker, workers)
        buildable_pos = []
        for poss_move in possible_moves:
            for direction in self.DIRECTIONS:
                new_pos = self._add_pos_and_move(poss_move, direction)
                if self._can_pos_be_moved_to(new_pos, workers):
                    buildable_pos.append(new_pos)
        return buildable_pos

