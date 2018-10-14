#!/usr/bin/python3.6
import diagonal_placement_strategy
import unittest

class DiagonalPlacementStrategy(unittest.TestCase):

    place_strat = diagonal_placement_strategy.DiagonalPlacementStrategy()

    def setUp(self):
        self.players = [[(2,1), (3,2)], [(3,5), (5, 5)]]

    # teardown doesn't need to do anything
    def teardown(self):
        pass

    # tests worker placement if there aren't any opponents defined
    def test_placement_no_workers(self):
        self.players[1] = [None, None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 0))

    # tests where worker is placed in first position on diagonal
    def test_placement_first_on_diagonal(self):
        self.players[1] = [(0, 0), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (1, 1))

    # tests where worker is not placed in first position on diagonal
    def test_placement_first_on_diagonal(self):
        self.players[1] = [(1, 1), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 0))

        self.players[1] = [(2, 2), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 0))

        self.players[1] = [(5, 5), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 0))

    # tests where workers are placed starting from the first on the diagonal
    def test_placement_on_diagonal(self):
        self.players[1] = [(0, 0), (1, 1)]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (2, 2))

        self.players[0] = [(2, 2), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (3, 3))

if __name__ == '__main__':
    unittest.main()
