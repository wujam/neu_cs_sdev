#!/usr/bin/python3.6
import board
import unittest
import rulechecker

class TestRulesChecker(unittest.TestCase):
    rule_checker = None
    test_board = None

    squares = [[1,2,3,2,3,4],
              [1,1,1,1,1,1],
              [2,2,2,2,3,2],
              [1,1,1,1,1,1],
              [2,2,2,2,2,0],
              [3,3,3,2,3,2]]

    players = [[(2,1), (3,2)], [(3,5), (5, 5)]]

    def setUp(self):
        self.test_board = board.Board()
        for x in range(6):
            for y in range(6):
                self.test_board.set_floor_height(x, y, self.squares[y][x])

        self.rule_checker = rulechecker.RuleChecker(self.test_board)

    # doens't really need to do anything
    def teardown(self):
        pass

    def _place_workers(self):
        self.test_board.set_worker(*self.players[0][0], 1, 1)
        self.test_board.set_worker(*self.players[0][1], 1, 2)
        self.test_board.set_worker(*self.players[1][0], 2, 1)
        self.test_board.set_worker(*self.players[1][1], 2, 2)

    # tests if a move is valid when there are no workers
    def test_is_move_and_build_valid_no_workers(self):
        self.assertFalse(self.rule_checker.is_move_and_build_valid(1, 1, (0, 1), (0, 1)),\
            msg="A move on a board with no workers should be invalid")

    # tests if a move is valid when there are less than 4 workers
    def test_is_move_and_build_valid_some_workers(self):
        self.test_board.set_worker(*self.players[0][0], 1, 1)
        self.assertFalse(self.rule_checker.is_move_and_build_valid(1, 1, (0, 1), (0, 1)),\
            msg="A move on a board with less than 4 workers should be invalid")

    # tests if one valid move on a board is valid
    def test_is_move_and_build_valid_one_move(self): 
        self._place_workers()

        self.assertTrue(self.rule_checker.is_move_and_build_valid(2, 2, (-1, -1), (-1, -1)),\
            msg="Single move of Player 2 Worker 2 from (5,5) to (4,4) building "\
            "on (3, 3), building height 2 to building height 2 was expected to "\
            "be valid but was invalid")

    # tests failure cases of moving a worker out of bounds
    def test_is_move_and_build_valid_move_out_of_bound(self):
        self._place_workers()

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (1, 0), (-1, 0)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (6, 5) building "\
            "on (5, 5), should be invalid as the worker move is out of bounds")

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (1, 1), (-1, -1)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (6, 6) building "\
            "on (5, 5), should be invalid as the worker move is out of bounds")

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (0, 1), (0, -1)),\
            msg="Singel move of Player 2 Worker 2 from (5, 5) to (5, 6) building" \
            "on (5, 5), should be invalid as the worker move is out of bounds")

    # tests failure cases of building out of bounds
    def test_is_move_and_build_valid_build_out_of_bound(self):
        self._place_workers()

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (-1, 0), (0, 1)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (4, 5) building "\
            "on (4, 6), should be invalid as the building is out of bounds")

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (0, -1), (1, 0)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (5, 4) building "\
            "on (6, 4), should be invalid as the building is out of bounds")

    # tests failure cases of moving a worker onto buildings that are too high
    def test_is_move_and_build_valid_worker_onto_too_high_building(self):
        self._place_workers()

        self.assertFalse(self.rule_checker.is_move_and_build_valid(1, 1, (0, -1), (-1, 0)),\
            msg="Single move of Player 1 Worker 1 from (2, 1) to (2, 0) building "\
            "on (1, 0), building height 1 to building height 3 was expected to be"\
            "invalid, but was valid")

    # tests valid move onto building of 1 greater height
    def test_is_move_and_build_valid_worker_onto_higher_building(self):
        self._place_workers()

        self.assertTrue(self.rule_checker.is_move_and_build_valid(2, 2, (-1, 0), (0, -1)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (4, 5) building "\
            "on (4, 4), building height 2 to building height 3 was expected to "\
            "be valid but was invalid")

    # tests failure case of moving onto a spot where a worker already is
    def test_is_move_and_build_valid_moving_onto_another_worker(self):
        self._place_workers()

        self.test_board.set_worker(4, 5, 2, 2)

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (-1, 0), (0, -1)),\
            msg="Single move of Player 2 Worker 2 from (4, 5) to (3, 5) building "\
            "on (3, 4), moving to a space where another worker is was expected"\
            "to be invalid (moving onto another worker), but was valid")

    # tests failure case of building onto a spot where another worker already is
    def test_is_move_and_build_valid_building_onto_another_worker(self):
        self._place_workers()

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (-1, 0), (-1, 0)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (4, 5) building "\
            "on (3, 5), building on a space where another worker is was expected to be"\
            "invalid, but was valid")

    # tests failure case of moving onto a building with MAX height
    def test_is_move_and_build_valid_moving_onto_max_height_building(self):
        self._place_workers()

        self.test_board.set_worker(4, 0, 1, 2)

        self.assertFalse(self.rule_checker.is_move_and_build_valid(1, 2, (1, 0), (0, 1)),\
            msg="Single move of Player 1 Worker 2 from (4, 0) to (5, 0) building "\
            "on (5, 1), building height 3 to building height 4 was expected to be "\
            "invalid (building height too high), but was valid")

    # tests failure case of moving onto a building with MAX height
    def test_is_move_and_build_valid_building_onto_max_height_building(self):
        self._place_workers()

        self.test_board.set_worker(4, 0, 1, 2)

        self.assertFalse(self.rule_checker.is_move_and_build_valid(1, 2, (0, 1), (1, -1)),\
            msg="Single move of Player 1 Worker 2 from (4, 0) to (4, 1) building "\
            "on (5, 0), building height 4 to building height 5 was expected to be"\
            "invalid (building height too high), but was valid")

#    # test failure case of moving to a non neighboring space
#    def test_is_move_and_build_valid_building_onto_a_non_neighboring_space(self):
#        self._place_workers()
#
#        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (-2, 0), (-1, 0)),\
#            msg="Single move of Player 2 Worker 2 from (5, 5) to (3, 5) building "\
#            "on (2, 5), moving worker to a non-neighboring square was expected to be"\
#            "invalid, but was valid")


#    # test failure case of building onto a non neighboring building of the space moved to
#    def test_is_move_and_build_valid_building_onto_a_non_neighboring_building(self):
#        self._place_workers()
#
#        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (-1, 0), (-2, 0)),\
#            msg="Single move of Player 2 Worker 2 from (5, 5) to (4, 5) building "\
#            "on (2, 5), building on a non-neighboring square of the square of the "\
#            "square moved to was expected to be invalid, but was valid")

    # test failure case of moving worker onto itself
    def test_is_move_and_build_valid_moving_onto_self(self):
        self._place_workers()

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (0, 0), (-1, 0)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (5, 5) building "\
            "on (4, 5), moving worker onto itself was expected to be invalid, but was valid")

    # test failure case of building on spot just moved to
    def test_is_move_and_build_valid_building_onto_self(self):
        self._place_workers()

        self.assertFalse(self.rule_checker.is_move_and_build_valid(2, 2, (-1, 0), (0, 0)),\
            msg="Single move of Player 2 Worker 2 from (5, 5) to (4, 5) building "\
            "on (4, 5), building on the square a worker just moved to was expected to "\
            "be invalid, but was valid")

if __name__ == '__main__':
    unittest.main()
