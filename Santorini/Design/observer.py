"""Interface for a Observer if a game being refereeed in Santorini."""
from abc import ABC, abstractmethod


class AbstractStrategy(ABC):
    """interface for a Referee object in Santorini."""

    @abstractmethod
    def update(self, state):
        """Receieve an event and update the view based on the given state.

        :param Board state: a copy of the current game board
        """
        pass

    def update_game_over(self, state):
        """Same as the update event but this notifies the observer that the
        game is over as well.


        :param Board state: a copy of the current game board
        """
        pass
