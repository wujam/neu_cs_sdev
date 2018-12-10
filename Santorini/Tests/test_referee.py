"""Unit tests for the Referee Component."""

import unittest
from unittest import mock
import sys
import os
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Admin.referee import Referee, PlayerResult
from Santorini.Admin.observermanager import ObserverManager
from Santorini.Observer.observer import Observer
from Santorini.Common.player_guard import PlayerGuard
#from Santorini.Player.player import Player
from Santorini.Tests.player_mocks import *
import uuid
import time


class TestReferee(unittest.TestCase):

    def setUp(self):
        self.uuidp1 = uuid.uuid4()
        self.uuidp2 = uuid.uuid4()
        self.obs_man = ObserverManager()
        self.p1name = "p1"
        self.p2name = "p2"
        self.uuids_to_name = {self.uuidp1:self.p1name, self.uuidp2:self.p2name}

    # test the outcome of a game between two players using the diagonal placement
    # and the tree strategy

    @unittest.skip("test works but takes a while")
    def test_normal_game(self):
        """test a normal game between two good players
        """

        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)

        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)
        bad_players, game_results = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_called_once_with("p1")
        self.assertEqual(bad_players, [])
        self.assertEqual(game_results, [self.uuidp1])

    @unittest.skip("test works but takes a while")
    def test_normal_run_n_games(self):
        """test a normal game series between two good players
        """

        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)

        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)
        bad_players, game_results= ref.run_n_games(3)

        self.assertEqual(player1.end_of_game.call_count, 3)
        self.assertEqual(player2.end_of_game.call_count, 3)
        player1.end_of_game.assert_called_with("p1")
        player2.end_of_game.assert_called_with("p1")
        self.assertEqual(bad_players, [])
        self.assertEqual(game_results, [self.uuidp1, self.uuidp2, self.uuidp1])

    def test_game_invalid_placements(self):
        """test that a player who gives invalid placements loses
        test that end_of_game is called on both players
        """

        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()

        player2 = BadPlacementPlayer()
        player2.end_of_game = mock.MagicMock()

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)

        result = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()

        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_n_games_invalid_placements(self):
        """tests that a player who gives invalid placements
        always loses in a series of n games but all games are played
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()

        player2 = BadPlacementPlayer()
        player2.end_of_game = mock.MagicMock()

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)
        result = ref.run_n_games(3)

        self.assertEqual(player1.end_of_game.call_count, 1)
        self.assertEqual(player2.end_of_game.call_count, 0)
        player1.end_of_game.assert_called_with("p1")

        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_game_invalid_turn(self):
        """test that a player who passes an invalid turn loses immediately
        test that end_of_game is called on both players
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()

        player2 = BadTurnPlayer()
        player2.end_of_game = mock.MagicMock()

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)

        result = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_n_games_invalid_turns(self):
        """tests that a player who gives invalid turns
        always loses in a series of n games but all games are played
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()

        player2 = BadTurnPlayer()
        player2.end_of_game = mock.MagicMock()

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)
        result = ref.run_n_games(3)

        self.assertEqual(player1.end_of_game.call_count, 1)
        self.assertEqual(player2.end_of_game.call_count, 0)
        player1.end_of_game.assert_called_with("p1")
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_game_malformed_placement(self):
        """tests that a player who gives a malformed placement
        loses and end_of_game is not called on it
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.place_worker = mock.MagicMock(return_value="lolol")

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)

        result = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_n_games_malformed_placement(self):
        """tests that a player who gives a malformed placement
        loses and end_of_game is not called on it in n games
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")
        player2.place_worker = mock.MagicMock(return_value="lolol")

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)
        result = ref.run_n_games(3)

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_games_malformed_turn(self):
        """tests that a player who gives a malformed turn
        loses and end_of_games is not called on it
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.play_turn = mock.MagicMock(return_value="lolol")

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)

        result = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)


    def test_n_games_malformed_turn(self):
        """tests that a player who gives a malformed turn
        loses and end_of_games is not called on it in n games
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")
        player2.play_turn = mock.MagicMock(return_value="lolol")

        player1guard = PlayerGuard(player1)
        player2guard = PlayerGuard(player2)
        uuids_to_player = {self.uuidp1:player1guard, self.uuidp2:player2guard}
        ref = Referee(uuids_to_player, self.uuids_to_name, self.obs_man)

        result = ref.run_n_games(3)

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)


class testRefereeExceptionsTimeout(unittest.TestCase):
    """class that rests the referee when the player
    throws exceptions"""

    def take_time(self):
        time.sleep(10)

    def setUp(self):
        self.p1name = "p1"
        self.uuidp1 = uuid.UUID('00000000000000000000000000000000')
        self.player1 = LegitPlayer()
        self.player1.end_of_game = mock.MagicMock()
        self.player1.get_name = mock.MagicMock(return_value=self.p1name)

        self.p2name = "p2"
        self.uuidp2 = uuid.UUID('11111111111111111111111111111111')
        self.player2 = LegitPlayer()
        self.player2.end_of_game = mock.MagicMock()
        self.player2.get_name = mock.MagicMock(return_value=self.p2name)

        self.obs_man = ObserverManager()
        self.uuids_to_name = {self.uuidp1:self.p1name, self.uuidp2:self.p2name}
        self.player1guard = PlayerGuard(self.player1)
        self.player2guard = PlayerGuard(self.player2)
        self.uuids_to_player = {self.uuidp1:self.player1guard, self.uuidp2:self.player2guard}
        self.ref = Referee(self.uuids_to_player, self.uuids_to_name, self.obs_man)

    def test_start_of_game_exception(self):
        """tests that a player who throws an exception
        in start_of_game gets booted
        """
        self.player2.start_of_game = mock.MagicMock(side_effect=Exception())
        result = self.ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_set_id_exception(self):
        """tests that a player who throws an exception
        in start_of_game gets booted
        """
        self.player2.set_id = mock.MagicMock(side_effect=Exception())
        result = self.ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_place_worker_exception(self):
        """tests that a player who throws an exception
        in get_name gets booted
        """
        self.player2.place_worker = mock.MagicMock(side_effect=Exception())
        result = self.ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)


    def test_end_of_game_exception(self):
        """tests that a player who throws an exception
        in get_name gets booted
        """
        self.player2.play_turn = mock.MagicMock(side_effect=Exception())
        result = self.ref.run_game()

        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_start_of_game_timeout(self):
        """tests that a player who throws an timeout
        in start_of_game gets booted
        """
        self.player2.start_of_game = mock.MagicMock(side_effect=self.take_time)
        result = self.ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_set_id_timeout(self):
        """tests that a player who throws an timeout
        in start_of_game gets booted
        """
        self.player2.set_id = mock.MagicMock(side_effect=self.take_time)
        result = self.ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_place_worker_timeout(self):
        """tests that a player who throws an timeout
        in get_name gets booted
        """
        self.player2.place_worker = mock.MagicMock(side_effect=self.take_time)
        result = self.ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)

    def test_end_of_game_timeout(self):
        """tests that a player who throws an timeout
        in get_name gets booted
        """
        self.player2.play_turn = mock.MagicMock(side_effect=self.take_time)
        result = self.ref.run_game()

        bad_players, game_results = result
        expected_bad_players = [self.uuidp2]
        for actual, expected in zip(bad_players, expected_bad_players):
            self.assertEqual(actual, expected)
        expected_game_results = [self.uuidp1]
        for actual, expected in zip(game_results, expected_game_results):
            self.assertEqual(actual, expected)
