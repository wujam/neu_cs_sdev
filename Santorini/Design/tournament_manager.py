import sys
"""Interface for a tournament manager of multiple games of Santorini for multiple workers"""

class TournamentManager:


    def run_tournament():
        """Runs a round robin tournament against the configured players

        A game result is a 2 element list with the first element being the
        name of the winner and the second being the name of the loser

        :rtype (List of names of misbehaving players,
               list of game results in the order played):

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

    def read_config_from(self, file_in=sys.stdin):
        """Reads the tournament configuration from a given io object
        To read in a config file pass in a file objects with a file open
        
        The input io should contain a json text with the following contents
        { "players"    : [[Kind, Name, PathString, ...]],
          "observers"  : [[Name, PathString], ...]
        }
        a Kind is one of: "good" for a well behaved player
                          "breaker" for a player that terminates correctly but misbehaves
                          "infinite" for a player that goes into an infinite loop
        a Name is a JSON String denoting the name of the player
        a PathString is Linux Path to the implementation of the player/observer
        :param TextIOBase file_in: Defaults to stdin. A source of text to read from.

        Steps to load up the configuration:
         - Read the players from the player list
         - Load up the player objects and wrap them in player_guards
         - hand each player a UUID and set the maps of UUIDs to player_guard and UUIDs to player_name
           - if a player_guard reports an error while setting the UUID don't include this player
            in the tournament
           - while setting names in the UUID to name map make sure that the names are unique
         - Load up the observer objects from the 
        """
        pass
