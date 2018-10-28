"""
Implementation of a PlayerGuard 

Wraps a player and throws custom exceptions beased
on various player failure states.
"""
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
        super().__init__(value)
    def __str__(self):
        super().__str__()

class PlayerMalformedData(PlayerError):
    # Exception for when a player returns malformed data
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        super().__str__()

class PlayerTimeout(PlayerError):
    # Exception for when a player takes too long to return
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        super().__str__()

class PlayerUnownedWorker(PlayerError):
    # Exception for when a player returns a worker they don't own
    def __init__(self, value):
        super().__init__(value)
    def __str__(self):
        super().__str__()

class PlayerGuard():

    def __init__(self, player, timeout=5):
        """
        :param Player player: the Player to wrap
        :param int timeout: the number of seconds that calls should timeout after 
        """
        self.player = player

    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        pass

    def get_name(self):
        """Get a name to call this Player.
        :rtype String name, a name that this player wants to call itself.
        """
        pass

    def start_of_game(self):
        """
        Runs the start of game function of a player and returns the data
        or raises a corresponding PlayerError
        """
        pass

    def place_worker(self, cur_board):
        """Worker Placement.
        
        Run the place_worker method of a player and returns the data
        or raises a corresponding PlayerError

        :param Board cur_board: a copy of the current board
        """
        pass

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        Runs the start of game function of a player and returns the data
        or raises a corresponding PlayerError

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        pass

    def game_over(self, winner):
        """Call when the game is over.

        Runs the start of game function of a player and returns the data
        or raises a corresponding PlayerError

        :param str winner: the name of the Player that won the game
        """
        pass
