import sys
"""Interface for a tournament manager of multiple games of Santorini for multiple workers"""

class TournamentManager:
    def run_tournament():
        """Runs a round robin tournament against the configured players
        :rtype List of Players winners: list of players who win the tournament

        To start the round robin tournament we need to generate the list of
        matches that will be played in the tournament.

        This generation of the list of possible matches can be done by
        all unique pairs of different players and keeping track of
        which pairs have played against each other as the tournament goes on.
        Also keep track of how many wins each player has as the tournament
        goes on.

        Matches should be opportunistically started as the tournament continues

        Multiple matches can occur simultaneously
        so long as the players starting a new match aren't already in a game that
        is in progress.

        The tournament is over once all possible matches have been played and at that
        point run_tournament should return a list of players who had the highest scores

        Broken players should be removed from the tournament when they break
        Matches involving them shouuld be removed from the list of possible matches
        and their scores should be removed list of scores.
        """
        pass

    def read_config_from(file_in=sys.stdin):
        """Reads the tournament configuration from an input file source
        
        The input string should be a json text with the following contents
        { "players"    : [[Kind, Name, PathString, ...]],
          "observers"  : [[Name, PathString], ...]
        }
        a Kind is one of: "good" for a well behaved player
                          "breaker" for a player that terminates correctly but misbehaves
                          "infinite" for a player that goes into an infinite loop
        a Name is a JSON String denoting the name of the player
        a PathString is Linux Path to the implementation of the player/observer
        :param TextIOBase file_in: Defaults to stdin. A source of text to read from.
        """
        pass
