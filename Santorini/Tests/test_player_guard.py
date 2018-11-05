"""Unit tests for the Board Component."""
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import *
from Santorini.Tests.player_mocks import *
from Santorini.Admin.player_guard import *
import uuid

class TestPlayerGuard(unittest.TestCase):
    """Player Guard Unit Tests"""
    def setUp(self):
        pass

    def test_legit_player(self):
        """ Test that correct moves go through """
        board = Board()
        player1 = LegitPlayer()
        player2 = LegitPlayer()
        player_guard1 = PlayerGuard(player1)
        player_guard2 = PlayerGuard(player2)

        # set ids
        p1id = uuid.uuid4()
        p2id = uuid.uuid4()
        player_guard1.set_id(p1id)
        player_guard2.set_id(p2id)

        # test methods don't error out
        player_guard1.start_of_game()
        player_guard2.start_of_game()
        board.place_worker(*player_guard1.place_worker(board))
        board.place_worker(*player_guard2.place_worker(board))
        board.place_worker(*player_guard2.place_worker(board))
        board.place_worker(*player_guard1.place_worker(board))
        player_guard1.play_turn(board)
        player_guard2.play_turn(board)
        player_guard1.end_of_game("legit player")
        player_guard2.end_of_game("legit player")

    def test_bad_placement(self):
        """ Test that well formed bad placements raise PlayerInvalidPlacement """
        board = Board()
        player1 = LegitPlayer()
        player2 = BadPlacementPlayer()
        player_guard1 = PlayerGuard(player1, timeout=3)
        player_guard2 = PlayerGuard(player2, timeout=3)

        # set ids
        p1id = uuid.uuid4() 
        p2id = uuid.uuid4() 
        player_guard1.set_id(p1id)
        player_guard2.set_id(p2id)

        board.place_worker(*player_guard1.place_worker(board))

        self.assertRaises(PlayerInvalidPlacement, player_guard2.place_worker, board)

    def test_bad_turn(self):
        """ Test that well formed bad turns raise PlayerInvalidTurn """
        board = Board()
        player1 = LegitPlayer()
        player2 = BadTurnPlayer()
        player_guard1 = PlayerGuard(player1)
        player_guard2 = PlayerGuard(player2)

        # set ids
        p1id = uuid.uuid4() 
        p2id = uuid.uuid4() 
        player_guard1.set_id(p1id)
        player_guard2.set_id(p2id)

        board.place_worker(*player_guard1.place_worker(board))
        board.place_worker(*player_guard2.place_worker(board))
        board.place_worker(*player_guard2.place_worker(board))
        board.place_worker(*player_guard1.place_worker(board))

        self.assertRaises(PlayerInvalidTurn, player_guard2.play_turn, board)

    def test_bad_worker(self):
        """ Test that unowned worker placement gives the correct Exception """
        board = Board()
        player1 = LegitPlayer()
        player2 = BadWorkerPlayer()
        player_guard1 = PlayerGuard(player1, timeout=3)
        player_guard2 = PlayerGuard(player2, timeout=3)

        # set ids
        p1id = uuid.uuid4() 
        p2id = uuid.uuid4() 
        player_guard1.set_id(p1id)
        player_guard2.set_id(p2id)

        board.place_worker(*player_guard1.place_worker(board))
        self.assertRaises(PlayerUnownedWorker, player_guard2.place_worker, board)

    def test_exception_player(self):
        """ Test that players who throw exceptions get filtered to our Exception """
        board = Board()
        player1 = ExceptionPlayer()
        player_guard1 = PlayerGuard(player1, timeout=3)

        # set ids
        p1id = uuid.uuid4() 
        self.assertRaises(PlayerRaisedException, player_guard1.set_id, p1id)

        self.assertRaises(PlayerRaisedException, player_guard1.start_of_game)
        self.assertRaises(PlayerRaisedException, player_guard1.place_worker, board)
        self.assertRaises(PlayerRaisedException, player_guard1.play_turn, board)
        self.assertRaises(PlayerRaisedException, player_guard1.end_of_game, "player")

    def test_loop_player(self):
        """ Test that players who get stuck in an infinite loop are timed out
            and a timeout exception is thrown"""
        board = Board()
        player1 = LoopPlayer()
        player_guard1 = PlayerGuard(player1, timeout=1)

        # set ids
        p1id = uuid.uuid4() 
        self.assertRaises(PlayerTimeout, player_guard1.set_id, p1id)

        self.assertRaises(PlayerTimeout, player_guard1.start_of_game)
        self.assertRaises(PlayerTimeout, player_guard1.place_worker, board)
        self.assertRaises(PlayerTimeout, player_guard1.play_turn, board)
        self.assertRaises(PlayerTimeout, player_guard1.end_of_game, "player")

    def test_sleep_player(self):
        """ Test that players who stall for time (sleep) are timed out and
            a timeout exception is thrown"""
        board = Board()
        player1 = SleepPlayer()
        player_guard1 = PlayerGuard(player1, timeout=1)

        p1id = uuid.uuid4() 
        self.assertRaises(PlayerTimeout, player_guard1.set_id, p1id)

        self.assertRaises(PlayerTimeout, player_guard1.start_of_game)
        self.assertRaises(PlayerTimeout, player_guard1.place_worker, board)
        self.assertRaises(PlayerTimeout, player_guard1.play_turn, board)

    def test_malformed_player(self):
        """ Test that players who return malformed data give the correction Exception """
        board = Board()
        player1 = MalformedDataPlayer()
        player_guard1 = PlayerGuard(player1, timeout=3)

        p1id = uuid.uuid4()

        player_guard1.set_id(uuid.uuid4())

        self.assertRaises(PlayerMalformedData, player_guard1.place_worker, board)
        self.assertRaises(PlayerMalformedData, player_guard1.play_turn, board)
