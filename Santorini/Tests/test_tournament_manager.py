"""Unit tests for the Direction Component."""
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Admin.tournament_manager import TournamentManager
import io


"""
Example config format:
{ "players"   : [[Kind, Name, PathString], ..., [Kind, Name, PathString]],
  "observers" : [[Name, PathString], ..., [Name, PathString]]  }
"""


class TestTournamentManager(unittest.TestCase):

    def setUp():
        self.tm = TournamentManager()

    def testRegularConfiguration(self):
        """Tests that a tournament manager sets state correctly from a regular
           Players should be set correctly and so should observers
        """

        in_out = io.StringIO('{ "players" : '\
                                '[["good", "a", "./player_mocks/legit_player.py"],'\
                                '["good", "b", "./player_mocks/legit_player.py"]]'\
                                '{ "observers" : '\
                                '[["bobserver", "../Observer/bbserver.py"]]')

        self.tm.read_config_from(file_in=in_out)

        player_guards = tm._get_player_guards()

    def testMultipleNameConfiguration(self):
        """Tests that a tournament manager gives players who have the same name
           unique names
        """

        in_out = io.StringIO('{ "players" : '\
                                '[["good", "a", "./player_mocks/legit_player.py"],'\
                                '["good", "a", "./player_mocks/legit_player.py"]]'\
                                '{ "observers" : '\
                                '[["bobserver", "../Observer/bbserver.py"]]')

        self.tm.read_config_from(file_in=in_out)

    def testTournamentMalformedPlayer(self):
        """Tests a tournament manager with a malformed player
           The malformed player should be removed from the tournament
        """

    def testTournamentInfinitePlayer(self):
        """Tests a tournament with an infinitely looping player
           The infinitely looping player should be removed from the tournament
        """

    def testTournamentTwoInfinitePlayers(self):
        """Tests a tournament with two infinitely looping players as the first two players
           They should be the first two players so they both error out
        """
