"""Interface for a Strategy in Santorini."""
from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
    """interface for a strategy object in Santorini."""

    @abstractmethod
    def plan_placement(self, player, board):
        """Generate a plan for the next turn to be played.

        :param Uuid player: the Player calling this method 
        :param Board board: a copy of the current game board
        :rtype tuple result: a tuple, position (row, col),
                            representing the placement on the board
        """
        pass

    @abstractmethod
    def plan_turn(self, workers, board):
        """Generate a plan for the next turn to be played.
        A valid turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param list workers: the workers of the Player calling this method 
        :param Board board: a copy of the current game board
        :rtype Union[(None, None, None), (Worker, Direction, None),
                     (Worker, Direction, Direction)]:
               a valid turn as described above
        """
        pass
