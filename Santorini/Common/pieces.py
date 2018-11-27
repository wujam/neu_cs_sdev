#!/usr/bin/env python36
"""Santorini game pieces implementation."""
from operator import add
from enum import Enum
import json

class Board:
    """Board implementation for Santorini."""

    # Board dimensions are 6x6
    BOARD_SIZE = 6

    def __init__(self, board=None, workers=None):
        """Create a 6x6 board. with 0-floor buildings in each cell.

        _board is a 2-d array of Buildings representing the Santorini board,

        _workers is a dictionary of Workers to Position (ROW, COLUMN) on board
        """
        if board:
            self._board = []
            for row in range(self.BOARD_SIZE):
                self._board.append([])
                for col in range(self.BOARD_SIZE):
                    try:
                        height = board[row][col]
                    except IndexError:
                        height = 0
                    self._board[row].append(Building(height))
        else:
            self._board = [[Building() for col in range(self.BOARD_SIZE)]
                           for row in range(self.BOARD_SIZE)]

        if workers:
            self._workers = workers
        else:
            self._workers = {}

    @property
    def workers(self):
        """Return the list of workers on this board."""
        return list(self._workers.keys())

    def assert_bounds(self, pos):
        """Raise an exception if the position is out of bounds.

        :param tuple (row, col): A position on the game board
        :raises IndexError: if the position is outside of the board
        range [0,BOARD_SIZE)
        """
        row, col = pos

        if not (row in range(self.BOARD_SIZE) and
                col in range(self.BOARD_SIZE)):
            raise IndexError("Cannot place a worker out of board bounds")

    def place_worker(self, worker, pos):
        """Place a worker in a starting position on the board.

        This method updates the current dictionary of workers
        to set the input worker's position to the new input
        pos

        :param Worker worker: a Worker object
        :param tuple (row, col): a position on the board
        :raises IndexError: if the position is outside of the board
        range [0,BOARD_SIZE)
        """
        self.assert_bounds(pos)
        self._workers[worker] = pos

    def move_worker(self, worker, direction):
        """Move a worker to a new position on the board.

        This method updates the worker's position
        in the internal dictionary to the new position
        calculated from the input direction

        *a Worker *must* be placed before it can move
        *This does not check if a worker can move there.

        :param Worker worker: a Worker on the board
        :param Direction direction: a Direction on the board
        :raise IndexError: if the calculated position is outside the bounds of
        the board#
        :raise LookupError: if the worker is not found on the board (i.e. in
        the _workers dict)
        :raise ValueError: if the calculated position is already occupied by
        another Worker
        """
        pos = self.worker_position(worker)
        cur_pos = Direction.move_position(pos, direction)
        self.assert_bounds(cur_pos)
        self._workers[worker] = cur_pos

    def build_floor(self, worker, direction):
        """Build one floor of a building at a position.

        build_floor adds a single floor to the given position.
        All valid positions on the board are buildings, starting
        at 0 floors. Increments the Building's floor counter by one

        Building on a position that already has 4 floors does nothing.

        :param Worker worker: a Worker on the board
        :param Direction direction: a Direction on the board
        :raise IndexError: if the calculated position is outside the bounds of
        the board
        :raise LookupError: if the worker is not found on the board (i.e. in
        the _workers dict)
        """
        pos = self.worker_position(worker)
        row, col = Direction.move_position(pos, direction)
        self.assert_bounds((row, col))
        self._board[row][col].build()

    def get_height(self, position, direction):
        """Get the height of a building.

        The height of a building is obtained from getting the
        input worker's position and adding the input direction to it

        :param tuple(row, col) position: a position on the board
        :param Direction direction: a Direction on the board
        :rtype int: the building height at the position
        :raise IndexError: if the calculated position is outside the bounds of
        the board
        """
        row, col = Direction.move_position(position, direction)
        self.assert_bounds((row, col))
        return self._board[row][col].floor

    def is_maxheight(self, position, direction):
        """Return if location from worker pos & dir is at max height.

        :param Worker worker: a Worker on the board
        :param Direction direction: the direction the Worker is interested in
        :rtype bool: True if the desired building is at max height
        """
        row, col = Direction.move_position(position, direction)
        self.assert_bounds((row, col))
        return self._board[row][col].is_max_height()

    def worker_position(self, worker):
        """Return the position of the given worker as a (row, col).

        If the worker isn't found on the board, return None

        :param Worker worker: a Worker on the board

        :rtype tuple pos | None: the position (row, col) on the board
        the worker is at
        """
        return self._workers.get(worker)

    def is_occupied(self, pos):
        """Check if the current location is occupied by a Worker or out of bounds.

        :param Position (row, col): the position to check against
        :rtype bool: Returns if the position is not occupied and valid
        """
        return any([p == pos for p in self._workers.values()])

    def is_neighbor(self, worker, direction):
        """Check if the input worker has a neighbor.

        :param Worker worker: a Worker on the board
        :param Direction direction: the Direction the Worker wants to move
        :raises KeyError: if the worker is not in the dictionary
        :rtype bool
        """
        try:
            pos = self.worker_position(worker)
            self.assert_bounds(Direction.move_position(pos, direction))
        except IndexError:
            return False
        return True

    def dump_as_json(self, id_to_name):
        """
        Gives a Json representation of the board.
        :param map{Uuid -> String} id_to_name: map of uuids to player name
        :rtype 2D List of string or int: a 2D list representing the board
                                         which can be dumped to json
        """
        tiles = []
        for i in range(self.BOARD_SIZE):
            tiles.append([])
            for j in range(self.BOARD_SIZE):
                tiles[i].append(self.get_height((i, j), Direction.STAY))

        for w in self.workers:
            row, col = self.worker_position(w)
            tiles[row][col] = str(tiles[row][col]) + w.dump_with_name(id_to_name)

        return tiles

    def dump_workers_as_json(self, id_to_name):
        """
        Gives a Json representation of the workers on the board
        :param map{Uuid -> String} id_to_name: map of uuids to player name
        :rtype List of WorkerPlace: List of worker placements
        """
        worker_placements = []
        for w in self.workers:
            worker = w.dump_with_name(id_to_name)
            row, col = self._workers[w]
            worker_placements.append([worker, row, col])
        return worker_placements


    def __str__(self):
        """Give a readable string representation of this board.
        :rtype str
        """
        return "Board: " + str(self._board) + " Workers: " + str(self._workers.items())

class Building:
    """A game piece representing a building in Santorini."""

    # Maximum height of a building is four
    MAX_HEIGHT = 4

    def __init__(self, floor=0):
        """Create a building with 0 floors."""
        self._floor = floor

    def build(self):
        """Build a floor in the current building.

        Increments floor each time this is called if the number
        of floors in this building is less than four.

        :rtype int returns the new height of the building
        :raise OverflowError: if a Worker tries to add a fifth
        floor to a building
        """
        if self.is_max_height():
            raise OverflowError(f"Cannot build over {self.MAX_HEIGHT}")
        else:
            self._floor += 1

    @property
    def floor(self):
        """Return number of floors in the building."""
        return self._floor

    def is_max_height(self):
        """Return True if it is at the max height."""
        return self._floor == self.MAX_HEIGHT

    def __repr__(self):
        """Returns a unambiguous representation of a building
        :rtype str
        """
        return str(self._floor)

class Worker:
    """A game piece representing a worker in Santorini."""

    NUM_WORKERS = 2

    def __init__(self, player, num):
        """Create a worker.

        Worker will be associated with the player and the piece number
        given as inputs
        :param Uuid player: the player this piece is associated with
        :param int num: the piece number [1 - NUM_WORKERS]
        :raises ValueError when num is out of range [1 - NUM_WORKERS]
        """
        self._player = player
        if num in range(1, self.NUM_WORKERS + 1):
            self._num = num
        else:
            raise ValueError("Worker number out of range!")

    @property
    def player(self):
        """Return the player the worker belongs to."""
        return self._player

    @property
    def number(self):
        """Return the piece number of the worker."""
        return self._num


    def dump_with_name(self, id_to_name):
        """
        Gives a string representation of a worker in json.
        :param map{Uuid -> String} id_to_name: map of uuids to player name
        :rtype String: a string representing the worker that can be dumped
                       to json
        """
        return str(id_to_name[self.player]) + str(self._num)

    def __eq__(self, other):
        """Worker piece equality."""
        if not isinstance(other, Worker):
            return False
        return (self._player == other.player and
                self._num == other.number)

    def __hash__(self):
        """Worker piece hashing."""
        return hash((self._player, self._num))

    def __repr__(self):
        """Return a readable string representation of a worker
        rtype: str
        """
        return str(self._player) + str(self._num)

class Direction(Enum):
    """Represents a direction in the eight cardinal directions.

    First entry in tuple is ROW, second entry is COLUMN

    STAY is equivalent of not moving to a new position
    """

    NORTH = (-1, 0)
    NORTHEAST = (-1, 1)
    NORTHWEST = (-1, -1)
    SOUTH = (1, 0)
    SOUTHEAST = (1, 1)
    SOUTHWEST = (1, -1)
    EAST = (0, 1)
    WEST = (0, -1)
    STAY = (0, 0)

    def __init__(self, row, col):
        """Create the Direction."""
        self.row = row
        self.col = col

    @property
    def vector(self):
        """Return the vector representation of the direction as (x, y)."""
        return (self.row, self.col)

    @staticmethod
    def move_position(pos, direction):
        """Return the new position as (row, col) given a direction to move in.

        :param pos (row, col):
        :param Direction direction:
        """
        pos = tuple(map(add, pos, direction.vector))
        return pos

    def string_values(self):
        """Return Direction as a list of strings, EAST or WEST and NORTH or SOUTH
        :rtype list of string
        """
        east_west_map = {
            0  : "PUT",
            1  : "EAST",
            -1 : "WEST"
        }

        north_south_map= {
            0  : "PUT",
            1  : "SOUTH",
            -1 : "NORTH"
        }

        return [east_west_map[self.col], north_south_map[self.row]]

    def __str__(self):
        x, y = self.string_values()

        return x + "," + y


DIR_TABLE = {("PUT", "NORTH"): Direction.NORTH,
             ("PUT", "SOUTH"): Direction.SOUTH,
             ("PUT", "PUT"): Direction.STAY,
             ("EAST", "PUT"): Direction.EAST,
             ("WEST", "PUT"): Direction.WEST,
             ("EAST", "NORTH"): Direction.NORTHEAST,
             ("WEST", "NORTH"): Direction.NORTHWEST,
             ("EAST", "SOUTH"): Direction.SOUTHEAST,
             ("WEST", "SOUTH"): Direction.SOUTHWEST}
