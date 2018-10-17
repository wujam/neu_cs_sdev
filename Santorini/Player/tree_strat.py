"""A game tree-based strategy to be used with a Player component in Santorini."""

import copy
from itertools import product

from Santorini.Player.strategy import TurnStrategy
from Santorini.Common.pieces import Direction
from Santorini.Common import rulechecker


class TreeStrategy(TurnStrategy):
    """A strategy implementation that uses a game tree to ensure that
    the opponent cannot make a winning move given a depth to look-ahead
    in the tree
    """

    def __init__(self, depth=2):
        """Constructs a Game-tree turn strategy object with the
        look-ahead depth

        :param int depth: the amount of turns to lookahead (defaults to 2)
        """
        self.depth = depth

    @staticmethod
    def next_turn(workers, board):
        """Creates a generator that yields the next possible
        turn given a list of workers and board

        :param list Worker workers: A list of workers belonging
                                    to the same player
        :param Board board: A game board
        :rtype Generator[(Worker, Direction, Direction), None None]
        """
        for worker in workers:
            for move_dir in Direction:
                if (rulechecker.can_move_build(board, worker,
                                               move_dir)):
                    yield (worker, move_dir, None)
            for move_dir, build_dir in product(Direction, Direction):
                if (rulechecker.can_move_build(board, worker,
                                               move_dir, build_dir)):
                    yield (worker, move_dir, build_dir)

    @staticmethod
    def do_survive(board, pname, depth, worker=None,
                   move_dir=None, build_dir=None):
        """Given a game state, and a look-ahead depth and an
        optional turn, return whether or not the given player name
        survives up to the depth number of rounds.

        :param Board board: A game board
        :param str pname: A player name
        :param int depth: the number of look-ahead rounds
        :param Worker worker: an optional worker to move and/or build
        :param Direction move_dir: The direction to move the given
                                   worker if a worker was given
        :param Dircetion build_dir: An optional direction the worker builds in
        :rtype bool: if we survived depth number of rounds
        """
        copied_board = copy.deepcopy(board)
        if move_dir:
            copied_board.move_worker(worker, move_dir)
            if build_dir:
                copied_board.build_floor(worker, build_dir)

        # if we won, we survived
        if rulechecker.get_winner(copied_board) == pname:
            return True

        # base case, if there's no winner, we survived
        if depth == 0:
            return not rulechecker.get_winner(copied_board)

        # recursive case
        opp_workers = [w for w in copied_board.workers
                       if pname != w.player]
        enemy_turns = TreeStrategy.next_turn(opp_workers, copied_board)
        for enemy_worker, enemy_move, enemy_build in enemy_turns:
            next_board = copy.deepcopy(copied_board)
            next_board.move_worker(enemy_worker, enemy_move)
            if enemy_build:
                next_board.build_floor(enemy_worker, enemy_build)
            winner = rulechecker.get_winner(next_board)
            if (winner and winner != pname):
                return False
        return TreeStrategy.do_survive(board, pname, depth - 1)

    def get_turn(self, workers, board):
        """Return a valid turn for the list of player's worker on the board.

        A valid turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param list Worker workers: A list of a player's worker
        :param Board board: a game board

        :rtype Union[(None, None, None), (Worker, Direction, None),
                     (Worker, Direction, Direction)]:
               a valid turn as described above
        """
        turn = (None, None, None)
        for worker, move_dir, build_dir in TreeStrategy.next_turn(workers,
                                                                  board):
            if TreeStrategy.do_survive(board, workers[0].player, self.depth,
                                       worker, move_dir, build_dir):
                turn = (worker, move_dir, build_dir)
                break
        return turn
