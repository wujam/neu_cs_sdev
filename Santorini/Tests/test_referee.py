"""Unit tests for the PlacementStrat Component."""
import unittest
import sys
import os
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Admin.referee import Referee
from Santorini.Player.player import Player


class TestReferee(unittest.TestCase):
    """Test diagonal placement strategy"""

    def setUp(self):
        self.player1 = Player("one")
        self.player2 = Player("two")

    def test_game(self):
        ref = Referee([self.player1, self.player2])

        self.assertEqual(ref.run_game(), self.player2)
