"""
Interface for a PlayerGuard 

Wraps a player and throws custom exceptions beased
on various player failure states.
"""
from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class PlayerError(Exception):
    # General Player Exception Class
    def __init__(self, vlaue):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PlayerRaisedException(PlayerError):
    # Exception for when the player raises an exception
    def __init__(self, value):
        super(value)
    def __str__(self):
        super()

class PlayerMalformedData(PlayerError):
    # Exception for when a player returns malformed data
    def __init__(self, value):
        super(value)
    def __str__(self):
        super()

class PlayerTimeout(PlayerError):
    # Exception for when a player takes too long to return
    def __init__(self, value):
        super(value)
    def __str__(self):
        super()

class PlayerUnownedWorker(PlayerError):
    # Exception for when a player returns a worker they don't own
    def __init__(self, value):
        super(value)
    def __str__(self):
        super()

class AbstractPlayerGuard(ABC):

    def __init__(self, player, timeout):
        """
        :param Player player: the Player to wrap
        :param int timeout: the number of seconds that calls should timeout after 
        """
        self.player = player

    @abstractmethod
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        pass

    @abstractmethod
    def get_name(self):
        """Get a name to call this Player.
        :rtype String name, a name that this player wants to call itself.
        """
        pass

    @abstractmethod
    def start_of_game(self):
        """
        Runs the start of game function of a player and returns the data
        or raises a correspinding PlayerError
        """
        pass

    @abstractmethod
    def place_worker(self, cur_board):
        """Worker Placement.
        
        Run the place_worker method of a player and returns the data
        or raises a corresponding PlayerError

        :param Board cur_board: a copy of the current board
        """
        pass

    @abstractmethod
    def play_turn(self, cur_board):
        """Regular Santorini turn.

        Runs the start of game function of a player and returns the data
        or raises a correspinding PlayerError

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        pass

    @abstractmethod
    def game_over(self, winner):
        """Call when the game is over.

        Runs the start of game function of a player and returns the data
        or raises a correspinding PlayerError

        :param str winner: the name of the Player that won the game
        """
        pass
