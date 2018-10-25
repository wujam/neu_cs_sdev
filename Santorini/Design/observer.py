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
    def update_placement(self, board, placement, worker_to_player)
        """Receives a placement and updates

        A placement is a tuple of worker and
        positon (in the form ( Worker, (row, col)),

        :param Board board: a copy of the current game board
        :param placement placement: a turn that the player inputted
        :param worker_to_player dict: dict mapping worker to player names
        """

    @abstractmethod
    def update_turn(self, board, turn, worker_to_player):
        """Receives a turn and updates.

        A turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param Board board: a copy of the current game board
        :param turn turn: a turn that the player inputted
        :param worker_to_player dict: dict mapping worker to player names
        """
        pass

    @abstractmethod
    def update_game_over(self, board):
        """Same notifies the observer that the game is over as well.


        :param Board board: a copy of the current game board
        :param player string: name of the player that won
        """
        pass
