"""Interface for a referee in Santorini."""
from abc import ABC, abstractmethod

class PlayerResult(Enum):
    """ Describes a result of a player interaction """
    OK = 0
    GIVE_UP = 1
    BAD = 2
    NEFARIOUS = 3

class AbstractReferee(ABC):
    """Interface for a Referee component in Santorini."""

    def __init__(self, uuids_players, uuids_names, observer_manager):
        """Create a referee component with the associated list of players.
        :param dict[UUID -> Player] uuids_players: dictionary of UUIDs to players
        :param dict[UUID -> String] uuids_names: dictionary of UUIDs to player names
        :param ObserverManager observer_manager: an observer manager object
        :param int timeout: time in seconds allowed per player action
        """
        self.players = players

    @abstractmethod
    def run_game(self):
        """Supervise a game between players.

        A referee will be able to construct a new board and have
        access to the rules. The ref will then initialize each player
        and then determine the "first" player in the game.

        The ref will receive the player's worker placements and then
        place them, in alternating order, on the board.

        During the course of the game, the ref will call complete_turn
        to execute turns given to him by the player.

        If a game end state is reached, the ref will call determine_winner
        to check against its list of players and the board to get the
        winner of the game. 

        :rtype tuple(list(Uuid), list(Uuid))
            The first list is a list of misbehaving players in order
            The second list contains the Uuid of the winner of the game,
            if both players are disqualified this list is empty.
        """
        pass

    @abstractmethod
    def run_n_games(self, num_games):
        """Supervise num_games games between players.

        The referee runs n games and returns the Uuid of the player who won
        the most games.

        :param int num_games: the number of games to run, must be non-negative
                                and odd
        :rtype tuple(list(Uuid), list(Uuid))
            The first list is a list of misbehaving players in order
            The second list contains the Uuid of the winner of each game played in order,
            if both players are disqualified this list is empty.
        """
        pass

    @abstractmethod
    def add_observer(self, observer):
        """Adds an observer, which will be sent the board, placements,
        turns, errors, and gameover in a timely manner.
        :param Observer observer: an Observer for this game
        """
        pass
