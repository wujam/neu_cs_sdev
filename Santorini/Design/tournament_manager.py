"""Interface for a tournament manager of multiple games of Santorini for multiple workers"""

"""Takes in a list of players to run a round robin tournament against the players
:param List of Players players: list of players to run the tournament with, must have at least 2 players
:rtype List of Players winners: list of players who win the tournament"""
def run_tournament(players):
    """
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
