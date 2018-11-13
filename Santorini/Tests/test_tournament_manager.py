"""Unit tests for the Tournament Manager Component."""
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Admin.tournament_manager import TournamentManager
import io
import uuid


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
                                '["good", "a", "./Tests/player_mocks/legit_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "./Observer/observer.py"]]}')

        self.tm.read_config_from(file_in=json_config)
        player_names = self.tm.uuids_names.values()
        self.assertEqual(len(player_names), 2)
        player_name_set = set()
        player_name_set.update(player_names)
        self.assertEqual(len(player_name_set), 2)

    def testTournament(self):
        """Tests that a tournament manager with 2 good players runs correctly"""
        json_config = io.StringIO('{ "players" : '\
                                '[["good", "a", "./Tests/player_mocks/legit_player.py"],'\
                                '["good", "b", "./Tests/player_mocks/legit_player.py"]],'\
                                '"observers" : '\
                                '[]}')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 2)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, [])
        self.assertEqual(meetups, [["a", "b"]])

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

    @unittest.skip("test works but takes a while")
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

    @unittest.skip("test works but takes a while")
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

    @unittest.skip("to fix")
    def testTournamentMalformedJSON(self):
        """Tests that a coniguration is ignored if it is bad JSON"""

        json_config = io.StringIO('{ "players" : ')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 0)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, [])
        self.assertEqual(meetups, [])

    @unittest.skip("to fix")
    def testTournamentMalformedConfig(self):
        """Tests that a coniguration is ignored if it is not well-formed"""

        json_config = io.StringIO('{"players" : []}')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 0)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, [])
        self.assertEqual(meetups, [])

    def testTournamentBadPaths(self):
        """Tests that a config with bad paths skips the item that's bad"""

        json_config = io.StringIO('{ "players" : '\
                                '[["good", "a", "not a path"],'\
                                '["good", "b", "./Tests/player_mocks/legit_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "/root"]]}')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 1)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, [])
        self.assertEqual(meetups, [])

    @unittest.skip("to fix")
    def testTournamentBadPlayerSpec(self):
        """Tests that a config with bad paths skips the item that's bad"""

        json_config = io.StringIO('{ "players" : '\
                                '[["good", "a", "./Tests/player_mocks/legit_player.py"],'\
                                '["good", "./Tests/player_mocks/legit_player.py"]],'\
                                '"observers" : '\
                                '[["bobserver", "/root"]]}')

        self.tm.read_config_from(file_in=json_config)
        player_guards = self.tm.uuids_players.values()
        self.assertEqual(len(player_guards), 1)

        bad_players, meetups = self.tm.run_tournament()
        self.assertEqual(bad_players, [])
        self.assertEqual(meetups, [])

    def test_add_player(self):
        """Tests that _add_player adds a player correctly"""
        self.tm._add_player(["good", "a", "./Tests/player_mocks/legit_player.py"])
        self.tm._add_player(["good", "b", "./Tests/player_mocks/legit_player.py"])
        self.assertEqual(len(self.tm.uuids_players), 2)
        self.assertEqual(len(self.tm.uuids_names), 2)
        self.assertEqual(list(self.tm.uuids_names.values())[0], "a")
        self.assertEqual(list(self.tm.uuids_names.values())[1], "b")

    def test_add_player_bad_name(self):
        """Tests that _add_player doesn't add players with bad names"""
        self.tm._add_player(["good", "b0", "./Tests/player_mocks/legit_player.py"])
        self.assertEqual(len(self.tm.uuids_players), 0)

    def test_add_player_bad_path(self):
        """Tests that _add_player doesn't add players with bad paths"""
        self.tm._add_player(["good", "b0", "./Tests/player_mocks/legit_player.p"])
        self.assertEqual(len(self.tm.uuids_players), 0)

    def test_add_observer_bad_path(self):
        """Tests that _add_player doesn't add players with bad paths"""
        self.tm._add_player(["good", "b0", "./Tests/player_mocks/legit_player.p"])
        self.assertEqual(len(self.tm.uuids_players), 0)

    def test_validate_name(self):
        """Tests that _validate_name returns true on good names"""
        self.assertTrue(self.tm._validate_name("aaa"))
        self.assertTrue(self.tm._validate_name("bbb"))

    def test_validate_nameBadNames(self):
        """Tests that _validate_name returns true on good names"""
        self.assertFalse(self.tm._validate_name("aa_a"))
        self.assertFalse(self.tm._validate_name("bb0b"))
        self.assertFalse(self.tm._validate_name("bbJb"))
        self.assertFalse(self.tm._validate_name("bb:b"))
        self.assertFalse(self.tm._validate_name("bb b"))
        self.assertFalse(self.tm._validate_name(b'\x05\x02'.decode("ascii")))

    def test_gen_unique_name(self):
        """Tests that _gen_unique_name returns the same name given a unique name"""
        p1name = "alice"
        p2name = "bob"
        p3name = "cat"

        self.tm._add_player(["good", p1name, "./Tests/player_mocks/legit_player.py"])
        self.tm._add_player(["good", p2name, "./Tests/player_mocks/legit_player.py"])

        self.assertEqual(self.tm._gen_unique_name(p3name), p3name)

    def test_gen_uniqueNameNonUniqueName(self):
        """Tests that _gen_unique_name returns a unique name given a non unique name"""
        p1name = "alice"
        p2name = "bob"

        self.tm._add_player(["good", p1name, "./Tests/player_mocks/legit_player.py"])
        self.tm._add_player(["good", p2name, "./Tests/player_mocks/legit_player.py"])

        names = self.tm.uuids_names.values()
        new_name = self.tm._gen_unique_name(p2name)
        self.assertFalse(new_name in names)

    def test_winner_to_meet_up_result(self):
        """Tests that _winner_to_meet_up_results returns the correct player"""
        p1id = uuid.uuid4()
        p2id = uuid.uuid4()
        players = [p1id, p2id]

        self.assertEqual(self.tm._winner_to_meet_up_result(players, p1id),\
                         [p1id, p2id])
        self.assertEqual(self.tm._winner_to_meet_up_result(players, p2id),\
                         [p2id, p1id])

    def test_filter_bad_meet_up_results(self):
        """Tests that _winner_to_meet_up_results returns the correct player"""
        p1id = uuid.uuid4()
        p2id = uuid.uuid4()
        p3id = uuid.uuid4()
        p4id = uuid.uuid4()
        self.tm.meet_up_results = [[p2id, p1id], [p1id, p3id], [p1id, p4id],
                                   [p2id, p3id], [p2id, p4id], [p3id, p4id]]

        self.tm.nef_players = [p2id, p3id]

        self.tm._filter_bad_meet_up_results()
        self.assertEqual(self.tm.meet_up_results,
                         [[p1id, p2id], [p1id, p3id], [p1id, p4id],
                          [p4id, p2id], [p4id, p3id]])
