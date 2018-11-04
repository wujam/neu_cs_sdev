"""Unit tests for the Referee Component."""

import unittest
from unittest import mock
import sys
import os
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Admin.referee import Referee, PlayerResult
#from Santorini.Player.player import Player
from Santorini.Tests.player_mocks import *
import uuid
import time


class TestReferee(unittest.TestCase):

    def setUp(self):
        self.uuidp1 = uuid.uuid4()
        self.uuidp2 = uuid.uuid4()

    # test the outcome of a game between two players using the diagonal placement
    # and the tree strategy

    """
        def test_start_of_game_end_of_game_called_normal_game(self):
    """
    #test that start_of_game and end_of_game are called in a normal game
    #also tests how a game between two legit players would go
    """
            player1 = LegitPlayer()
            player1.start_of_game = mock.MagicMock()
            player1.end_of_game = mock.MagicMock()
            player1.get_name = mock.MagicMock(return_value="p1")

            player2 = LegitPlayer()
            player2.start_of_game = mock.MagicMock()
            player2.end_of_game = mock.MagicMock()
            player2.get_name = mock.MagicMock(return_value="p2")

            ref = Referee({self.uuidp1:player1, self.uuidp2:player2})
            result = ref.run_game()

            player1.start_of_game.assert_called_once()
            player2.start_of_game.assert_called_once()
            player1.end_of_game.assert_called_once_with("p1")
            player2.end_of_game.assert_called_once("p1")
            self.assertEqual(result, PlayerResult.OK,self.uuidp1)
    """
    """
        def test_run_n_games_normal_games(self):
    """
    #test start_of_game and end_of_game calls in normal
    #run_n_games series
    """
            player1 = LegitPlayer()
            player1.start_of_game = mock.MagicMock()
            player1.end_of_game = mock.MagicMock()
            player1.get_name = mock.MagicMock(return_value="p1")

            player2 = LegitPlayer()
            player2.start_of_game = mock.MagicMock()
            player2.end_of_game = mock.MagicMock()
            player2.get_name = mock.MagicMock(return_value="p2")

            ref = Referee({self.uuidp1:player1, self.uuidp2:player2})
            result = ref.run_n_games(3)

            self.assertEqualplayer1.start_of_game.call_count:3
            self.assertEqualplayer2.start_of_game.call_count:3
            self.assertEqualplayer1.endof_game.call_count:3
            self.assertEqualplayer2.end_of_game.call_count:3
            player1.end_of_game.assert_called_with("p1")
            player2.end_of_game.assert_called_with("p1")
            self.assertEqual(result, PlayerResult.OK,self.uuidp1)
    """
    def test_game_invalid_placements(self):
        """test that a player who gives invalid placements loses
        test that end_of_game is called on both players
        """
        
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = BadPlacementPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})

        result = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        self.assertEqual(result, (PlayerResult.NEFARIOUS, [self.uuidp2]))

    def test_n_games_invalid_placements(self):
        """tests that a player who gives invalid placements
        always loses in a series of n games but all games are played
        """
        player1 = LegitPlayer()
        player1.start_of_game = mock.MagicMock()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = BadPlacementPlayer()
        player2.start_of_game = mock.MagicMock()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})
        result = ref.run_n_games(3)

        self.assertEqual(player1.start_of_game.call_count, 1)
        self.assertEqual(player2.start_of_game.call_count, 1)
        self.assertEqual(player1.end_of_game.call_count, 1)
        self.assertEqual(player2.end_of_game.call_count, 0)
        player1.end_of_game.assert_called_with("p1")
        self.assertEqual(result, (PlayerResult.NEFARIOUS, [self.uuidp2]))

    def test_game_invalid_turn(self):
        """test that a player who passes an invalid turn loses immediately
        test that end_of_game is called on both players
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = BadTurnPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})

        result = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        self.assertEqual(result, (PlayerResult.NEFARIOUS, [self.uuidp2]))

    def test_n_games_invalid_turns(self):
        """tests that a player who gives invalid turns
        always loses in a series of n games but all games are played
        """
        player1 = LegitPlayer()
        player1.start_of_game = mock.MagicMock()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = BadTurnPlayer()
        player2.start_of_game = mock.MagicMock()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})
        result = ref.run_n_games(3)

        self.assertEqual(player1.start_of_game.call_count, 1)
        self.assertEqual(player2.start_of_game.call_count, 1)
        self.assertEqual(player1.end_of_game.call_count, 1)
        self.assertEqual(player2.end_of_game.call_count, 0)
        player1.end_of_game.assert_called_with("p1")
        self.assertEqual(result, (PlayerResult.NEFARIOUS, [self.uuidp2]))

    def test_game_malformed_placement(self):
        """tests that a player who gives a malformed placement
        loses and end_of_game is not called on it
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")
        player2.place_worker = mock.MagicMock(return_value="lolol")

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})
        self.assertEqual(len(ref.players), 2)
        self.assertEqual(len(ref.uuids_to_player.keys()), 2)

        result = ref.run_game()
        self.assertEqual(len(ref.players), 2)
        self.assertEqual(len(ref.uuids_to_player.keys()), 2)

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result2 = (res_enum, set(nef_players))
        self.assertEqual(result2, (PlayerResult.NEFARIOUS, {self.uuidp2}))

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

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})

        result = ref.run_n_games(3)

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_games_malformed_turn(self):
        """tests that a player who gives a malformed turn
        loses and end_of_games is not called on it
        """
        player1 = LegitPlayer()
        player1.end_of_game = mock.MagicMock()
        player1.get_name = mock.MagicMock(return_value="p1")

        player2 = LegitPlayer()
        player2.end_of_game = mock.MagicMock()
        player2.get_name = mock.MagicMock(return_value="p2")
        player2.play_turn = mock.MagicMock(return_value="lolol")

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})

        result = ref.run_game()

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

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

        ref = Referee({self.uuidp1:player1, self.uuidp2:player2})

        result = ref.run_n_games(3)

        player1.end_of_game.assert_called_once_with("p1")
        player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

class testRefereeExceptionsTimeout(unittest.TestCase):
    """class that rests the referee when the player
    throws exceptions"""

    def take_time(self):
        time.sleep(10)

    def setUp(self):
        self.uuidp1 = uuid.uuid4()
        self.player1 = LegitPlayer()
        self.player1.end_of_game = mock.MagicMock()
        self.player1.get_name = mock.MagicMock(return_value="p1")

        self.uuidp2 = uuid.uuid4()
        self.player2 = LegitPlayer()
        self.player2.end_of_game = mock.MagicMock()
        self.player2.get_name = mock.MagicMock(return_value="p2")

    def test_start_of_game_exception(self):
        """tests that a player who throws an exception
        in start_of_game gets booted
        """
        self.player2.start_of_game = mock.MagicMock(side_effect=Exception())
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2})
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_set_id_exception(self):
        """tests that a player who throws an exception
        in start_of_game gets booted
        """
        self.player2.set_id = mock.MagicMock(side_effect=Exception())
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2})
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_get_name_exception(self):
        """tests that a player who throws an exception
        in get_name gets booted
        """
        self.player2.get_name = mock.MagicMock(side_effect=Exception())
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2})
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_place_worker_exception(self):
        """tests that a player who throws an exception
        in get_name gets booted
        """
        self.player2.place_worker = mock.MagicMock(side_effect=Exception())
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2})
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_end_of_game_exception(self):
        """tests that a player who throws an exception
        in get_name gets booted
        """
        self.player2.play_turn = mock.MagicMock(side_effect=Exception())
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2})
        result = ref.run_game()

        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_start_of_game_timeout(self):
        """tests that a player who throws an timeout
        in start_of_game gets booted
        """
        self.player2.start_of_game = mock.MagicMock(side_effect=self.take_time)
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2}, timeout = 3)
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_set_id_timeout(self):
        """tests that a player who throws an timeout
        in start_of_game gets booted
        """
        self.player2.set_id = mock.MagicMock(side_effect=self.take_time)
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2}, timeout = 3)
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_get_name_timeout(self):
        """tests that a player who throws an timeout
        in get_name gets booted
        """
        self.player2.get_name = mock.MagicMock(side_effect=self.take_time)
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2}, timeout = 3)
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_place_worker_timeout(self):
        """tests that a player who throws an timeout
        in get_name gets booted
        """
        self.player2.place_worker = mock.MagicMock(side_effect=self.take_time)
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2}, timeout = 3)
        result = ref.run_game()

        self.player1.end_of_game.assert_called_once_with("p1")
        self.player2.end_of_game.assert_not_called()
        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))

    def test_end_of_game_timeout(self):
        """tests that a player who throws an timeout
        in get_name gets booted
        """
        self.player2.play_turn = mock.MagicMock(side_effect=self.take_time)
        ref = Referee({self.uuidp1:self.player1, self.uuidp2:self.player2}, timeout = 3)
        result = ref.run_game()

        res_enum, nef_players = result
        result = (res_enum, set(nef_players))
        self.assertEqual(result, (PlayerResult.NEFARIOUS, {self.uuidp2}))
