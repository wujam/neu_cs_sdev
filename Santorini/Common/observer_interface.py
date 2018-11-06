"""Interface for an Observer of a game being refereed in Santorini."""
from abc import ABC, abstractmethod


class AbstractObserver(ABC):
    """Interface for a Observer object in Santorini."""

    def __init__(self, referee):
        """Create an observer object that plugs into the referee
        
        The method should plug into the referee that it will observe
        in order to send and receive messages from it
        :param referee: the referee that this 
        """
        pass

    @abstractmethod
    def update_placement(self, board, placement, id_to_name):
        """Receives a placement and updates

        A placement is a tuple of worker and
        positon (in the form ( Worker, (row, col)),

        :param Board board: a copy of the current game board
        :param Placement placement: a turn that the player inputted
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        pass

    @abstractmethod
    def update_turn(self, board, turn, id_to_name):
        """Receives a turn and updates.

        A turn is one of:
        (None, None, None) - A give_up request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param Board board: a copy of the current game board
        :param Turn turn: a turn that the player inputted, cannot be a give up move (None, None, None)
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        pass

    def update_gave_up(self, player_name):
        """Receives a player who is giving up
        :param String player_name: name of the player who gave up
        """
        pass

    @abstractmethod
    def update_game_over(self, board, player, id_to_name):
        """Same notifies the observer that the game is over as well.


        :param Board board: a copy of the current game board
        :param player string: name of the player that won
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        pass

    @abstractmethod
    def update_error_msg(self, msg):
        """Takes a string that represents an error message
        prints out when a player mis-behaves

        :param str msg: the message as a string
        """
        pass
