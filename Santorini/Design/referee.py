"""Interface for a referee in Santorini."""
from abc import ABC, abstractmethod


class AbstractReferee(ABC):
    """Interface for a Referee component in Santorini."""
    class PlayerResult(Enum):
        """ Describes a result of a player interaction """
        OK = 0
        BAD = 1
        NEFARIOUS = 2

    def __init__(self, players, timeout=30):
        """Create a referee component with the associated list of players.
        :param list of tuple(Uuid, Player) players: uuids and the Player
                                                    they're assigned to
        :param int timeout: time in seconds allowed per player action
        """
        self.players = players
        self.timeout = timeout

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

        :rtype tuple(PlayerResult.OK, Uuid) the player won the game
               tuple(PlayerResult.NEFARIOUS, list(Uuid)) the player did something
                                                        untrustworthy and the
                                                        other should win by
                                                        default
        """
        pass

    @abstractmethod
    def run_n_games(self, num_games):
        """Supervise num_games games between players.

        The referee runs n games and returns the Uuid of the player who won
        the most games.

        :param int num_games: the number of games to run, must be non-negative
                                and odd
        :rtype tuple(PlayerResult.OK, Uuid) the player won the series
               tuple(PlayerResult.NEFARIOUS, list(Uuid)) the player did something
                                                   untrustworthy and the
                                                   other should win by
                                                   default
        """
        pass

    @abstractmethod
    def set_turn_timeout(self, timeout):
        """Sets a the turn timeout in seconds for the game administrated
        by this Referee.
        :param int timeout: Positive integer number of seconds. Players
                            who take longer than this to take an action
                            will be killed and assigned a game loss.
        """
        pass
