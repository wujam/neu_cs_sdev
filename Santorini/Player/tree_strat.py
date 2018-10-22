"""A game tree-based strategy to be used with a Player component in Santorini."""

import copy
from itertools import product

from Santorini.Player.strategy import TurnStrategy
from Santorini.Common.pieces import Direction
from Santorini.Common import rulechecker
import logging
logger = logging.getLogger('tree_strat')
logging.basicConfig(filename='tree_strat.log',level=logging.DEBUG)

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
        :param Direction build_dir: An optional direction the worker builds in
        :rtype bool: if we survived depth number of rounds
        """
        copied_board = copy.deepcopy(board)
        if move_dir:
            copied_board.move_worker(worker, move_dir)
            if build_dir:
                copied_board.build_floor(worker, build_dir)
            else:
                # if there's no build, you must win this turn
                return rulechecker.get_winner(copied_board) == pname

        checkwin = rulechecker.get_winner(copied_board)
        if checkwin == pname:
            # if we won, we survived
            logger.info(str(pname) + " won a case Board:" + str(board) + " at Depth:" + str(depth))
            depth -= 1
            return True
        elif checkwin:
            logger.info(str(pname) + " won a case Board:" + str(board) + " at Depth:" + str(depth))
            # if we lost, we died
            return False

        # base case, if there's no winner, we survived
        if depth == 0:
            logger.info("player" + pname + "lived with this move:" + str(copied_board) + " depth:" + str(depth))
            return not rulechecker.get_winner(copied_board)

        # recursive case
        opp_workers = [w for w in copied_board.workers
                       if pname != w.player]
        our_workers = [w for w in copied_board.workers
                       if pname == w.player]
        enemy_turns = TreeStrategy.next_turn(opp_workers, copied_board)
        viable_move = False
        if move_dir:
            for enemy_worker, enemy_move, enemy_build in enemy_turns:
                next_board = copy.deepcopy(copied_board)
                next_board.move_worker(enemy_worker, enemy_move)
                if enemy_build:
                    next_board.build_floor(enemy_worker, enemy_build)
                winner = rulechecker.get_winner(next_board)
                if (winner and winner != pname):
                    #enemy found a way to kill you on their move, return False
                    logger.info("player " + winner + " kills with this move:" + str(next_board) + " depth:" + str(depth))
                    return False

                if depth > 1:
                    our_turns = TreeStrategy.next_turn(our_workers, next_board)
                    safe = False
                    # check that we have a safe move
                    for our_worker, our_move, our_build in our_turns:
                        if TreeStrategy.do_survive(next_board, pname, depth - 2, worker=our_worker, move_dir=our_move, build_dir=our_build):
                            logger.info("player " + pname + " survived with this move:" + str(next_board) + " depth:" + str(depth))
                            continue
                        else:
                            safe = True
                            break
                    if safe:
                        viable_move = True
            # fell through
            # if depth was 1, that means that we were checking if the enemy could kill us, and if so that means this should
            # be True cause they failed to kill us
            # if depth was 2 or more that means searching for more moves failed, and we died
            logger.info("player " + pname +" depth:" + str(depth) + " viable_move" + str(viable_move))
            return depth < 2 or viable_move
        else:
            our_turns = TreeStrategy.next_turn(our_workers, copied_board)
            for our_worker, our_move, our_build in our_turns:
                if TreeStrategy.do_survive(copied_board, pname, depth - 2, worker=our_worker, move_dir=our_move, build_dir=our_build):
                    logger.info("player " + pname + " survived with this move:" + str(copied_board) + " depth:" + str(depth))
                    return True
            logger.info("player " + pname + " can't survive with this board:" + str(copied_board) + " depth:" + str(depth))
            return False

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
