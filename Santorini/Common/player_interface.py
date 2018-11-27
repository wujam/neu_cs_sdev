"""Interface for a Player in Santorini"""
from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


class AbstractPlayer(ABC):
    """Player interface."""

    @abstractmethod
    def set_id(self, player_id):
        """Give a id for this Player.

        :param Uuid player_id, this player's uuid
        """
        pass

    @abstractmethod
    def start_of_game(self):
        """Initialize the player.

        Called once at the start of the game to do any needed
        initializtion for the implementation of the player.
        """
        pass

    @abstractmethod
    def set_name(self, name, new_name=False):
        """Informs the player of their name

        Called to let the player know their name
        :param String name: the name of the this player
        :param Bool new_name: whether this name is a new name
        """
        pass

    @abstractmethod
    def set_opponent(self, opp_id, name):
        """Informs the player of the opponent's name

        Called at the start of a series of games to let player
        know the opponent's name
        """
        pass

    @abstractmethod
    def place_worker(self, cur_board):
        """Worker Placement.

        This will be called with a copy of the board when it is this player's
        turn to place.

        The board contains a dictionary of workers mapped to their positions,
        and each worker knows which player it is associated with. When a
        player places a worker, its position is updated in this dictionary in
        the next placement turn.
        The board also contains all of the heights of the buildings on the
        board. Interacting with this board *will not* change the current state
        of the board.

        To place a worker, the player will send the board state to the strategy
        object and receive a placement. A placement is a tuple of worker and
        positon (in the form ( Worker, (row, col)),
        representing the placement of a single worker on the board.

        After receiving this placement, the player will send this to the
        referee. If the placement is invalid or breaks the rules according
        to our defined rulechecker, the referee will call is_gameover and
        automatically declare the opposing player the winner.

        If the placement is valid, the referee will execute the placement and
        send back an updated version of the board for the next placement.

        When the placement is over, the referee will transition the player to a
        play turn when this player has both of its workers place and there are
        a total of four workers on the board.

        :param Board cur_board: a copy of the current board
        :rtype tuple (Worker, (row, col)) placement: the placement
        """
        pass

    @abstractmethod
    def play_turn(self, cur_board):
        """Regular Santorini turn.

        This will be called with a copy of the board when it is this player's
        turn.

        The board contains a dictionary of workers mapped to their positions,
        and each worker knows which player it is associated with.

        The board also contains all of the heights of the buildings on the
        board

        Interacting with this board *will not* change the current state of the
        board

        To play a turn, the player will send the board state to the strategy
        object and receive a turn.

        A valid turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        After creating this turn, the player will send this to the referre.
        If the turn is invalid or breaks the rules according to our defined
        rulechecker,the referee will call is_gameover and automatically declare
        the opposing player the winner.

        If the turn is valid, the referee will execute the move and build
        requests and send back an updated version of the board on the next
        turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        pass

    @abstractmethod
    def end_of_game(self, winner):
        """Call when the game is over.

        If any of the endgame conditions are met (see is_gameover method
        in the rulechecker interface), this will be sent to the game
        to determine the winner of the game.

        The game will send back which player's name won the game based on
        endgame conditions and return this name to the player to compare to
        itself.

        :param str winner: the name of the Player that won the game
        """
        pass
