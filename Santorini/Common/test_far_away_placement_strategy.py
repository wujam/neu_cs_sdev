#!/usr/bin/python3.6
import far_away_placement_strategy
import unittest

class TestFarAwayPlacementStrategy(unittest.TestCase):

    place_strat = far_away_placement_strategy.FarAwayPlacementStrategy()

    def setUp(self):
        self.players = [[(2,1), (3,2)], [(3,5), (5, 5)]]

    # teardown doesn't need to do anything
    def teardown(self):
        pass

    # tests worker placement if there aren't any opponents defined
    def test_placement_no_workers(self):
        self.players[1] = [None, None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 0))

    # tests where workers are placed if in corners
    def test_placement_in_two_corners(self):
        self.players[1] = [(0, 0), (0, 5)]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (5, 0))

    # tests where a worker is placed close to the center
    def test_placement_in_center(self):
        self.players[1] = [(2, 2), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (5, 5))

        self.players[1] = [(3, 3), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 0))

    # tests where a worker is placed in one corner
    def test_placement_one_corner(self):
        self.players[1] = [(0, 0), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (5, 5))

    # tests that a worker isn't placed where one already is
    def test_placement_not_on_another_worker(self):
        self.players[0] = [(5, 5), None]
        self.players[1] = [(0, 0), None]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (4, 5))

    # tests where a worker is placed when opponent workers are in opposing corners
    def test_placement_opposing_corners(self):
        self.players[1] = [(0, 0), (5, 5)]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 5))

        self.players[1] = [(5, 0), (0, 5)]
        self.assertEqual(self.place_strat.get_worker_placement(self.players), (0, 0))

if __name__ == '__main__':
    unittest.main()
