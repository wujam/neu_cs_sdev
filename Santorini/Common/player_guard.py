"""
Implementation of a PlayerGuard 

Wraps a player and throws custom exceptions beased
on various player failure states.
"""
import copy
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Lib.timeout import timeout
from Santorini.Common.pieces import *
from Santorini.Common import rulechecker

class PlayerError(Exception):
    # General Player Exception Class
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PlayerRaisedException(PlayerError):
    # Exception for when the player raises an exception
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return super().__str__()

class PlayerMalformedData(PlayerError):
    # Exception for when a player returns malformed data
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return super().__str__()

class PlayerTimeout(PlayerError):
    # Exception for when a player takes too long to return
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return super().__str__()

class PlayerUnownedWorker(PlayerError):
    # Exception for when a player returns a worker they don't own
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return super().__str__()

class PlayerInvalidTurn(PlayerError):
    # Exception for when a player makes an invalid turn 
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return super().__str__()

class PlayerInvalidPlacement(PlayerError):
    # Exception for when a player makes an invalid placement 
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        return super().__str__()

class PlayerGuard():

    NO_ID = -1
    PLACEMENT_LENGTH = 2
    POSITION_LENGTH = 2
    TURN_LENGTH = 3

    def __init__(self, player, timeout=60):
        """
        :param Player player: the Player to wrap
        :param Board board: a Board reference to the current game
        :param int timeout: the number of seconds that calls should timeout after 
        """
        self.player = player
        self.timeout = timeout
        self.player_id = self.NO_ID

    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """

        self._call_with_timeout(self.player.set_id, player_id)
        self.player_id = player_id

    def start_of_game(self):
        """
        Runs the start of game function of a player and returns the data
        or raises a corresponding PlayerError
        """
        self._call_with_timeout(self.player.start_of_game)

    def place_worker(self, cur_board):
        """Worker Placement.
        
        Run the place_worker method of a player and returns the data
        or raises a corresponding PlayerError

        :param Board cur_board: a copy of the current board
        :rtype Placement: the placement to be sent to the ref
        """
        placement = self._call_with_timeout(self.player.place_worker, cur_board)

        self._well_formed_placement(placement)
        self._valid_placement(placement, cur_board)
        return placement

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        Runs the start of game function of a player and returns the data
        or raises a corresponding PlayerError

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn: the turn to be sent to the ref.
        """
        turn = self._call_with_timeout(self.player.play_turn, cur_board)

        self._well_formed_turn(turn)
        self._valid_turn(turn, cur_board)
        return turn

    def end_of_game(self, winner):
        """Call when the game is over.

        Runs the start of game function of a player and returns the data
        or raises a corresponding PlayerError

        :param str winner: the name of the Player that won the game
        """
        self._call_with_timeout(self.player.end_of_game, winner)

    def _call_with_timeout(self, func, *args):
        """call a player function with timeout and general exception handling

        :param Function func: the function to call
        :param Tuple args: a tuple of arguments to call the function with
        :rtype rtype of func: the return of func
        :raises TimeoutError: if call takes too long 
        """
        try:
            with timeout(seconds = self.timeout):
                return func(*args)
        except TimeoutError:
            raise PlayerTimeout("")
        except:
            raise PlayerRaisedException("")

    def _well_formed_placement(self, placement):
        """Checks whether a given placement is well formed
        :param Placement placement
        :raises PlayerMalformedData: if placement is not a Placement
        """
        # check type and length of placement tuple
        if not isinstance(placement, tuple) or\
        len(placement) != self.PLACEMENT_LENGTH:
            raise PlayerMalformedData("")

        worker, position = placement
        # check worker and position
        self._well_formed_worker(worker)
        self._well_formed_position(position)

    def _valid_placement(self, placement, board):
        """Checks whether a given placement is valid
        :param Placement placement: placement to validate
        :param Board board: the board to validate against
        :raises PlayerInvalidPlacement: if placement is not valid
        """
        worker, position = placement
        if not rulechecker.can_place_worker(board, worker, position):
            raise PlayerInvalidPlacement("")

    def _well_formed_turn(self, turn):
        """Checks whether a given turn is well formed
        :param Turn turn
        :raises PlayerMalformedData: if turn is not a Turn
        """
        # check type and length of turn tuple
        if not isinstance(turn, tuple) or\
           len(turn) != self.TURN_LENGTH:
               raise PlayerMalformedData("")

        # check if turn is no move
        if turn == (None, None, None):
            return

        worker, move, build = turn

        self._well_formed_worker(worker)
        self._well_formed_direction(move)
        # check if the this is a move+build
        if build == None:
            return

        self._well_formed_direction(build)

    def _valid_turn(self, turn, board):
        """Checks whether a given turn is valid
        :param Turn turn: the Turn to validate 
        :param Board board: the board to validate against
        """
        if all(element is None for element in turn):
            return
        worker, move_dir, build_dir = turn
        can_move_build = rulechecker.can_move_build(copy.deepcopy(board), worker, move_dir, build_dir)
        if not can_move_build:
            raise PlayerInvalidTurn("")

    def _well_formed_direction(self, direction):
        """Checks whether a direction is well formed
        :param Direction direction: direction to check
        :raises PlayerMalformedData: if direction is not a Direction
        """
        # direction is an enum
        if not isinstance(direction, Direction):
            raise PlayerMalformedData("")

    def _well_formed_position(self, position):
        """Checks whether a position is well formed
        :param Tuple(int, int) position
        :raises PlayerMalformedData: if position is not a tuple of 2 ints
        """
        if not isinstance(position, tuple) or\
           len(position) != self.POSITION_LENGTH:
               raise PlayerMalformedData("")

        row, col = position
        # type check the position
        if not isinstance(row, int) or\
           not isinstance(col, int):
               raise PlayerMalformedData("")

    def _well_formed_worker(self, worker):
        """Checks whether a given worker is well formed
        :param Worker worker
        :raises PlayerMalformedData: if worker is not a Worker
        :raises PlayerUnownedWorker: if worker is not owned by the Player
        """
        # type check worker
        if not isinstance(worker, Worker):
            raise PlayerMalformedData("")

        # check that the worker's id is valid
        if worker.player != self.player_id:
            raise PlayerUnownedWorker("")

    def _well_formed_name(self, name):
        """Checks whether a given name is valid
        :param String name: name to check
        :raises PlayerMalformedData: if name is not a String
        """
        if not isinstance(name, str):
            raise PlayerMalformedData("")
