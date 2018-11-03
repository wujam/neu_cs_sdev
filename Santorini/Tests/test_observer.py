""" Tests for the Observer implementation """
import os
import unittest
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from io import StringIO

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

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def testUpdatePlacement(self):
        """ Test expected output of receiving a placement """
        with MockStdOut() as output:

        self.assertEquals(output[0], "blah")
        expected = 

