"""Unit tests for the Tournament Manager Component."""
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

    def setUp(self):
        self.tm = TournamentManager()

    def testRegularConfiguration(self):
        """Tests that a tournament manager sets state correctly from a regular
           Players should be set correctly and so should observers
        """

        json_config = io.StringIO('{ "players" : '\
                                '[["good", "a", "./Tests/player_mocks/legit_player.py"],'\
                                '["good", "b", "./Tests/player_mocks/legit_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "./Observer/observer.py"]]}')

        self.tm.read_config_from(file_in=json_config)

        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 2)

    def testMultipleNameConfiguration(self):
        """Tests that a tournament manager gives players who have the same name
           unique names
        """

        json_config = io.StringIO('{ "players" : '\
                                '[["good", "a", "./Tests/player_mocks/legit_player.py"],'\
                                '["breaking", "a", "./Tests/player_mocks/legit_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "./Observer/observer.py"]]}')

        self.tm.read_config_from(file_in=json_config)
        player_names = self.tm.uuids_names.values()
        self.assertEqual(len(player_names), 2)
        player_name_set = set()
        player_name_set.update(player_names)
        self.assertEqual(len(player_name_set), 2)

    def testTournamentMalformedPlayer(self):
        """Tests a tournament manager with a malformed player
           The malformed player should be removed from the tournament
        """
        json_config = io.StringIO('{ "players" : '\
                                '[["good", "a", "./Tests/player_mocks/legit_player.py"],'\
                                '["breaking", "b", "./Tests/player_mocks/malformed_data_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "./Observer/observer.py"]]}')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 2)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, ["b"])

    def testTournamentInfinitePlayer(self):
        """Tests a tournament with an infinitely looping player
           The infinitely looping player should be removed from the tournament
        """
        json_config = io.StringIO('{ "players" : '\
                                '[["good", "a", "./Tests/player_mocks/legit_player.py"],'\
                                '["infinite", "b", "./Tests/player_mocks/loop_placement_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "./Observer/observer.py"]]}')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 2)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, ["b"])

    def testTournamentTwoInfinitePlayers(self):
        """Tests a tournament with two infinitely looping players as the first two players
           They should be the first two players so they both error out
        """

        json_config = io.StringIO('{ "players" : '\
                                '[["infinite", "a", "./Tests/player_mocks/loop_placement_player.py"],'\
                                '["infinite", "b", "./Tests/player_mocks/loop_placement_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "./Observer/observer.py"]]}')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 2)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, ["a", "b"])

