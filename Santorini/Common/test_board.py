#!/usr/bin/python3.6
import board
import unittest

class TestBoard(unittest.TestCase):
    disboard = None

    squares = [[1,2,3,2,2,4],
              [1,1,1,1,1,1],
              [2,2,2,2,3,2],
              [1,1,1,1,1,1],
              [2,2,2,2,2,0],
              [3,3,3,2,3,2]]

    players = [[(2,1), (3,2)], [(3,5), (5, 5)]]

    
    def setUp(self):
        self.disboard = board.Board()
        for x in range(6):
            for y in range(6):
                self.disboard.set_floor_height(x, y, self.squares[y][x])

        self.disboard.set_worker(*self.players[0][0], 0, 0)
        self.disboard.set_worker(*self.players[0][1], 0, 1)
        self.disboard.set_worker(*self.players[1][0], 1, 0)
        self.disboard.set_worker(*self.players[1][1], 1, 1)

    # doens't really need to do anything
    def teardown(self):
        pass
        
    # testing whether set_worker actually sets workers correctly
    def set_worker(self):
        self.disboard.set_worker(0, 0, 0, 0)
        self.asssetEqual(self.disboard.get_worker_position(0, 0), (0, 0))

        self.disboard.set_worker(4, 3, 0, 1)
        self.asssetEqual(self.disboard.get_worker_position(0, 1), (4, 3))

        self.disboard.set_worker(4, 4, 1, 0)
        self.asssetEqual(self.disboard.get_worker_position(1, 0), (4, 4))

        self.disboard.set_worker(3, 5, 1, 1)
        self.asssetEqual(self.disboard.get_worker_position(1, 1), (3, 5))

    # testing if add_floor works up the required number of floors
    def test_add_floor(self):
        self.disboard.add_floor(5, 4)
        self.assertEqual(self.disboard.get_floor_height(5, 4), 1)
        self.disboard.add_floor(5, 4)
        self.assertEqual(self.disboard.get_floor_height(5, 4), 2)
        self.disboard.add_floor(5, 4)
        self.assertEqual(self.disboard.get_floor_height(5, 4), 3)
        self.disboard.add_floor(5, 4)
        self.assertEqual(self.disboard.get_floor_height(5, 4), 4)

        self.disboard.add_floor(1, 2)
        self.assertEqual(self.disboard.get_floor_height(1, 2), 3)

    # tests getting all floors on the board
    def test_get_floor_height(self):
        for x in range(self.disboard.BOARD_DIMENSION):
            for y in range(self.disboard.BOARD_DIMENSION):
                self.assertEqual(self.disboard.get_floor_height(x, y), self.squares[y][x])

    # test if set_floor_height can set the floor height to any allowed height
    def test_set_floor_height(self):
        self.disboard.set_floor_height(3, 2, 4)
        self.assertEqual(self.disboard.get_floor_height(3, 2), 4)

        self.disboard.set_floor_height(3, 2, 2)
        self.assertEqual(self.disboard.get_floor_height(3, 2), 2)

        self.disboard.set_floor_height(5, 0, 3)
        self.assertEqual(self.disboard.get_floor_height(5, 0), 3)

        self.disboard.set_floor_height(5, 0, 1)
        self.assertEqual(self.disboard.get_floor_height(5, 0), 1)

        self.disboard.set_floor_height(4, 4, 0)
        self.assertEqual(self.disboard.get_floor_height(4, 4), 0)

    # test getting worker_positions
    def test_get_worker_position(self):
        for i in range(2):
            for j in range(2):
                self.assertEqual(self.disboard.get_worker_position(i, j), self.players[i][j])

    def test_get_worker_positions(self):
        workers = self.disboard.get_worker_positions()

        for i in range(2):
            for j in range(2):
                self.assertEqual(workers[i][j], self.players[i][j])

    def test_get_buildiing_heights(self):
        buildings = self.disboard.get_building_heights()

        for x in range(self.disboard.BOARD_DIMENSION):
            for y in range(self.disboard.BOARD_DIMENSION):
                self.assertEqual(buildings[x][y], self.squares[y][x])

if __name__ == '__main__':
    unittest.main()
