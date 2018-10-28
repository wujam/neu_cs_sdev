"""Unit tests for the PlacementStrat Component."""
import unittest
import sys
import os
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Player.tree_strat import TreeStrategy as tree
from Santorini.Common.pieces import Board, Worker, Direction


class TestPlaceFarthest(unittest.TestCase):
    """Test farthest placement strategy."""

    def setUp(self):
        self.workers = [Worker("p1", 1),
                        Worker("p1", 2),
                        Worker("p2", 1),
                        Worker("p2", 2)]

    def test_plan_turn(self):
        """Test that plan_turn returns the correct turn
        for a simple test case."""
        board = Board([[2, 3]],
                      workers={self.workers[i]: (i, i)
                               for i in range(len(self.workers))})
        tree_strat = tree(2)
        self.assertEqual(tree_strat.plan_turn(self.workers[0:2], board),
                         (self.workers[0], Direction.EAST, None))

    def test_plan_turn_forced(self):
        """Test that plan_turn returns the correct turn
        for a simple test case."""
        board = Board([[2, 3],
                       [4, 0]],
                      workers={self.workers[i]: (i, i)
                               for i in range(len(self.workers))})
        tree_strat = tree(2)
        self.assertEqual(tree_strat.plan_turn(self.workers[0:2], board),
                         (self.workers[0], Direction.EAST, None))

    def test_depth_zero(self):
        """Test tree strategy for a depth of zero."""
        board = Board([[2, 3]],
                      workers={self.workers[i]: (i, i)
                               for i in range(len(self.workers))})
        self.assertTrue(tree.do_survive(board, "p1", 0, self.workers[0],
                                        Direction.EAST))
        self.assertTrue(tree.do_survive(board, "p1", 0, self.workers[0],
                                        Direction.SOUTH, Direction.NORTH))

    def test_depth_one(self):
        """Test tree strategy for a depth of one."""
        board = Board([[2, 3], [2, 2, 2, 2]],
                      workers={self.workers[i]: (1, i)
                               for i in range(len(self.workers))})
        self.assertTrue(tree.do_survive(board, "p1", 1, self.workers[1],
                                        Direction.NORTH))
        self.assertTrue(tree.do_survive(board, "p1", 1, self.workers[0],
                                        Direction.NORTH, Direction.EAST))
        self.assertFalse(tree.do_survive(board, "p1", 1, self.workers[0],
                                         Direction.SOUTH, Direction.EAST))
        self.assertFalse(tree.do_survive(board, "p1", 1, self.workers[1],
                                         Direction.SOUTH, Direction.EAST))

    def test_depth_one_again(self):
        """Test tree strategy for a depth of one again."""
        board = Board([[2, 3],
                       [2, 2, 2, 2],
                       [0, 1, 3, 2, 3, 1],
                       [0, 3, 2, 1, 2, 3]],
                      workers={self.workers[i]: (1, i)
                               for i in range(len(self.workers))})
        self.assertTrue(tree.do_survive(board, "p1", 1, self.workers[1],
                                        Direction.SOUTHEAST))
        self.assertFalse(tree.do_survive(board, "p1", 1, self.workers[0],
                                         Direction.SOUTH, Direction.EAST))
        self.assertTrue(tree.do_survive(board, "p2", 1, self.workers[2],
                                        Direction.SOUTH))

    def test_depth_two_example(self):
        """Test tree strategy for a depth of two.

        This is specifically the test Matthias posts on the project page.
        """
        board = Board([[0, 1, 3, 2],
                       [0, 2, 3]],
                      workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 1),
                               self.workers[2]: (0, 2),
                               self.workers[3]: (1, 1)})
        self.assertFalse(tree.do_survive(board, "p1",
                                         2, self.workers[1],
                                         Direction.SOUTHWEST,
                                         Direction.SOUTH))

    def test_depth_three_example(self):
        """Test tree strategy for a depth of three.

        This is specifically the test Matthias posts on the project page.
        """
        board = Board([[0, 0],
                       [3, 0]],
                      workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 1),
                               self.workers[2]: (2, 0),
                               self.workers[3]: (2, 1)})
        self.assertTrue(tree.do_survive(board, "p1",
                                        3, self.workers[0],
                                        Direction.SOUTHEAST,
                                        Direction.WEST))

    def test_depth2_boxin(self):
        """Test tree strategy for a depth of 2 on boxin config."""
        board = Board([[0, 0, 1, 0],
                       [0, 4, 4],
                       [4, 4]],
                      workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 1),
                               self.workers[2]: (0, 2),
                               self.workers[3]: (0, 3)})
        self.assertFalse(tree.do_survive(board, "p1",
                                         2, self.workers[1],
                                         Direction.SOUTHWEST,
                                         Direction.NORTHEAST))

    def test_depth1_boxin(self):
        """Test tree strategy for a depth of 2 on boxin config."""
        board = Board([[0, 0, 1, 0],
                       [0, 4, 4],
                       [4, 4]],
                      workers={self.workers[0]: (0, 0),
                               self.workers[1]: (0, 1),
                               self.workers[2]: (0, 2),
                               self.workers[3]: (0, 3)})
        self.assertFalse(tree.do_survive(board, "p1",
                                         1, self.workers[1],
                                         Direction.SOUTHWEST,
                                         Direction.NORTHEAST))

    def test_depth4(self):
        """Test tree strategy for a depth of 4."""
        board = Board(workers={self.workers[0]: (0, 0),
                               self.workers[1]: (1, 1),
                               self.workers[2]: (2, 2),
                               self.workers[3]: (3, 3)})
        self.assertTrue(tree.do_survive(board, "p1",
                                        4, self.workers[0]))
