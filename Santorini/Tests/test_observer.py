""" Tests for the Observer implementation """
import os
import unittest
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import Board, Worker, Direction
from Santorini.Observer.observer import Observer
from io import StringIO
import json
import uuid

class MockStdOut(list):
    def __enter__(self):
        self.str_io = StringIO()
        sys.stdout = self.str_io
        return self

    def __exit__(self, *args):
        self.extend(self.str_io.getvalue().splitlines())
        sys.stdout = sys.__stdout__
        del self.str_io

class TestObserver(unittest.TestCase):

    MOVE = "[{worker},{ew},{ns}]"
    MOVE_BUILD = "[{worker},{ew_move},{ns_move},{ew_build},{ns_build}]"

    PUT = "PUT"
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"

    def setUp(self):
        """Mock-up context for testing the observer"""

        self.ids = [uuid.uuid4(), uuid.uuid4()]
        self.player_names = ["player1", "player2"]
        self.uuids_to_name = { self.ids[0] : self.player_names[0],
                               self.ids[1] : self.player_names[1]}
        for player_id, player_name in zip(self.ids, self.player_names):
            self.uuids_to_name[player_id] = player_name
        self.workers = [Worker(self.ids[0], 1),
                        Worker(self.ids[0], 2),
                        Worker(self.ids[1], 1),
                        Worker(self.ids[1], 2)]

        self.observer = Observer()

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def testUpdatePlacement(self):
        """Test expected output of receiving a placement"""
        board = Board(
                workers= {
                    self.workers[0] : (0, 0)})

        with MockStdOut() as output:
            self.observer.update_placement(board, (0, 0), self.uuids_to_name)

        output_str = "".join(list(output))

        expected_json = [
                ["0player11", 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]

        self.assertEqual(json.loads(output_str), expected_json)

    def testUpdateWinMove(self):
        """Test expected output of receiving a winning move turn"""
        board = Board(
                board = [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 3, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
                workers = {
                   self.workers[0]: (0, 0),
                   self.workers[1]: (1, 1),
                   self.workers[2]: (2, 2),
                   self.workers[3]: (3, 4)})

        with MockStdOut() as output:
            self.observer.update_turn(board, 
                    (self.workers[3], Direction.EAST, None),
                    self.uuids_to_name)

        board_str = output[0]
        turn_str = output[1]

        expected_board_json = [
                ["0player11", 0, 0, 0, 0, 0],
                [0, "0player12", 0, 0, 0, 0],
                [0, 0, "0player21", 0, 0, 0],
                [0, 0, 0, 2, "3player22", 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]

        expected_turn_json = ["player22", "EAST", "PUT"]

        self.assertEqual(json.loads(board_str), expected_board_json)
        self.assertEqual(json.loads(turn_str), expected_turn_json)

    def testUpdateMoveBuildTurn(self):
        """Test expexted output of receiving a move+build turn"""

        board = Board(
                board = [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]],
                workers = {
                   self.workers[0]: (0, 0),
                   self.workers[1]: (1, 1),
                   self.workers[2]: (2, 2),
                   self.workers[3]: (3, 4)})

        with MockStdOut() as output:
            self.observer.update_turn(board, 
                    (self.workers[3], Direction.EAST, Direction.WEST),
                    self.uuids_to_name)

        board_str = output[0]
        turn_str = output[1]

        expected_board_json = [
                ["0player11", 0, 0, 0, 0, 0],
                [0, "0player12", 0, 0, 0, 0],
                [0, 0, "0player21", 0, 0, 0],
                [0, 0, 0, 1, "1player22", 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]

        expected_turn_json = ["player22", "EAST", "PUT", "WEST", "PUT"]

        self.assertEqual(json.loads(board_str), expected_board_json)
        self.assertEqual(json.loads(turn_str), expected_turn_json)

    def testUpdateGaveUp(self):
        name = "Tim"

        with MockStdOut() as output:
            self.observer.update_gave_up(name)

        output_str = "".join(list(output))

        self.assertEqual(json.loads(output_str),Observer.GIVE_UP_STR + name)

    def testUpdateGameOver(self):
        board = Board(
                workers = {
                   self.workers[0]: (0, 0),
                   self.workers[1]: (1, 1),
                   self.workers[2]: (2, 2),
                   self.workers[3]: (3, 3)})

        with MockStdOut() as output:
            self.observer.update_game_over(board, self.player_names[1], self.uuids_to_name)

        board_str = output[0]
        turn_str = output[1]

        expected_board_json = [
                ["0player11", 0, 0, 0, 0, 0],
                [0, "0player12", 0, 0, 0, 0],
                [0, 0, "0player21", 0, 0, 0],
                [0, 0, 0, "0player22", 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]

        self.assertEqual(json.loads(board_str), expected_board_json)

        self.assertEqual(json.loads(turn_str), Observer.WINNER_STR + self.player_names[1])

    def testUpdateErrorMsg(self):
        error = "player went haywire"

        with MockStdOut() as output:
            self.observer.update_error_msg(error)

        output_str = "".join(list(output))

        self.assertEqual(json.loads(output_str), Observer.ERROR_STR + error)
