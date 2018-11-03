"""Unit tests for the Direction Component."""
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import Direction


class TestDirection(unittest.TestCase):
    """Unit tests for the Direction."""

    def test_move_pos_north(self):
        """Testing moving north."""
        self.assertEqual(Direction.move_position((0, 0), Direction.NORTH),
                         (-1, 0))

    def test_move_pos_south(self):
        """Testing moving south."""
        self.assertEqual(Direction.move_position((0, 0), Direction.SOUTH),
                         (1, 0))

    def test_move_pos_east(self):
        """Testing moving east."""
        self.assertEqual(Direction.move_position((0, 0), Direction.EAST),
                         (0, 1))

    def test_move_pos_west(self):
        """Testing moving west."""
        self.assertEqual(Direction.move_position((0, 0), Direction.WEST),
                         (0, -1))

    def test_move_pos_northeast(self):
        """Testing moving northeast."""
        self.assertEqual(Direction.move_position((0, 0), Direction.NORTHEAST),
                         (-1, 1))

    def test_move_pos_northwest(self):
        """Testing moving northwest."""
        self.assertEqual(Direction.move_position((0, 0), Direction.NORTHWEST),
                         (-1, -1))

    def test_move_pos_southeast(self):
        """Testing moving southeast."""
        self.assertEqual(Direction.move_position((0, 0), Direction.SOUTHEAST),
                         (1, 1))

    def test_move_pos_southwest(self):
        """Testing moving southwest."""
        self.assertEqual(Direction.move_position((0, 0), Direction.SOUTHWEST),
                         (1, -1))

    def test_move_pos_stay(self):
        """Testing not moving."""
        self.assertEqual(Direction.move_position((0, 0), Direction.STAY),
                         (0, 0))

    def test_string_values_north(self):
        """Test string north"""
        dir_str = Direction.NORTH.string_values()
        self.assertEqual(dir_str, ["PUT", "NORTH"])

    def test_string_values_northeast(self):
        """Test string northeast"""
        dir_str = Direction.NORTHEAST.string_values()
        self.assertEqual(dir_str, ["EAST", "NORTH"])

    def test_string_values_northwest(self):
        """Test string northwest"""
        dir_str = Direction.NORTHWEST.string_values()
        self.assertEqual(dir_str, ["WEST", "NORTH"])

    def test_string_values_south(self):
        """Test string south"""
        dir_str = Direction.SOUTH.string_values()
        self.assertEqual(dir_str, ["PUT", "SOUTH"])

    def test_string_values_southeast(self):
        """Test string southeast"""
        dir_str = Direction.SOUTHEAST.string_values()
        self.assertEqual(dir_str, ["EAST", "SOUTH"])

    def test_string_values_southwest(self):
        """Test string southwest"""
        dir_str = Direction.SOUTHWEST.string_values()
        self.assertEqual(dir_str, ["WEST", "SOUTH"])

    def test_string_values_east(self):
        """Test string east"""
        dir_str = Direction.EAST.string_values()
        self.assertEqual(dir_str, ["EAST", "PUT"])

    def test_string_values_west(self):
        """Test string west"""
        dir_str = Direction.WEST.string_values()
        self.assertEqual(dir_str, ["WEST", "PUT"])

    def test_string_values_stay(self):
        """Test string stay"""
        dir_str = Direction.STAY.string_values()
        self.assertEqual(dir_str, ["PUT", "PUT"])
