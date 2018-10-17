#!/usr/bin/env python3.6
"""A Rule checker implementation for Santorini."""

from itertools import product
import sys
import os
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Santorini.Common.pieces import Building, Direction

# A build or move request is a (Worker, Direction)
#
# A Worker object is an instance of a worker on the board
# A Direction object is an instance of a cardinal direction on the board

TOTAL_WORKERS = 4
MOVE_HEIGHT_DIFFERENCE = 1


def valid_position(board, position):
    """Return the worker destination if it is valid on the board.

    If the position calculated from the worker and direction is
    invalid and occupied, return False

    :param Board board: a copy of the game board
    :param Worker worker: a Worker object
    :param Direction direction: a Direction object
    :rtype (row, col) | False
    """
    try:
        board.assert_bounds(position)
    except IndexError:
        return False
    return position and not board.is_occupied(position)


def height_difference(board, worker, direction):
    """Return if the worker can move in the direction.

    Direction must be within the height difference.
    """
    return (board.get_height(board.worker_position(worker), direction) -
            board.get_height(board.worker_position(worker), Direction.STAY) <=
            MOVE_HEIGHT_DIFFERENCE)


def can_place_worker(board, worker, position):
    """Return if you can place a worker at the position.

    :param Board board: a copy of the board
    :param Worker worker: a Worker to place
    :param tuple (row, col): a position to place the worker at
    """
    return (valid_position(board, position) and
            len(board.workers) < TOTAL_WORKERS and
            not board.worker_position(worker))


def can_move_build(board, worker, move_dir, build_dir=None):
    """Check if a worker can move and then build in the specified direction.

    :param Board board: a copy of the game board
    :param Worker worker: a Worker on the board
    :param Direction move_dir: A Direction to move in
    :param Direction build_dir: An (optional) Direction to build in
    """
    if move_dir == Direction.STAY or build_dir == Direction.STAY:
        return False
    moved_pos = Direction.move_position(board.worker_position(worker),
                                        move_dir)
    board_copy = copy.deepcopy(board)
    can_move = (valid_position(board_copy, moved_pos) and
                height_difference(board, worker, move_dir))
    if can_move:
        board_copy.move_worker(worker, move_dir)
    can_build = (not build_dir or
                 (valid_position(board_copy,
                                 Direction.move_position(moved_pos,
                                                         build_dir)) and
                  not board.is_maxheight(moved_pos, build_dir)))
    return can_move and can_build


def is_game_over(board, workers):
    """Determine if the game is over based on board state.

    Called by the referee after every move and build for a player
    If this is True at any point, after a move or build from any
    player, the referee ends the game

    Game-ending conditions:
    * A worker is on a building of height 3 = the player has won
    * A worker can move but not build = the game is not over
    * A worker can't move but can build = the game is not over

    :param Board board: a copy of the game board
    :param list workers: a list of Workers for the current player
    """
    turn_dict = {w: False for w in workers}
    for worker in workers:

        # If any of the workers are at a height of 3, the game is over
        if (board.get_height(board.worker_position(worker), Direction.STAY) ==
                Building.MAX_HEIGHT - 1):
            return True

        # If any of the workers can move or build in any direction, the game
        # is not over

        for move_dir in Direction:
            if can_move_build(board, worker, move_dir):
                break
        else:
            turn_dict[worker] = True

    return any(turn_dict.values())


def get_winner(board):
    """Return the winning player given the game board
    
    If there is no winning player, this will return false

    :param Board board: a copy of the game board
    :returns Player | False: player if there is a winner,
    false if the game isn't over yet
    """

    worker_status = {w.player: [] for w in board.workers}

    for worker in board.workers:
        worker_status[worker.player].append(False)

    for worker in board.workers:
        worker_pos = board.worker_position(worker)
        if board.get_height(worker_pos, Direction.STAY) == Building.MAX_HEIGHT - 1:
            return worker.player
        for move_dir in Direction:
            if can_move_build(board, worker, move_dir):
                worker_status[worker.player][worker.number - 1] = True

    for player in worker_status:
        if not any(worker_status[player]):
            return (worker_status.keys() - [player]).pop()
    return False
