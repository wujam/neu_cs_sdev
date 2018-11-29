import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import socket
import uuid
from enum import Enum, auto
from Santorini.Common.pieces import Board, Worker
from Santorini.Common.player_guard import PlayerGuard
from Santorini.Remote.client_messager import ClientMessager
from Santorini.Remote.jsonschemas import PLAYING_AS, NAME, PLACEMENT, RESULTS, OTHER, BOARD, RESULTS
from Santorini.Lib.json_validate import validate_json

class RelayState(Enum):
    """ An Enum representing the states of the proxy server relay
    """
    REGISTRATION = auto()
    PLACEMENT1 = auto()
    PLACEMENT2 = auto()
    TAKE_TURNS = auto()
    FINISHED = auto()

class RemoteProxyServer:

    def __init__(self, hostname, port, player, player_name):
        """ Create a connection to the server and setup PlayerGuard.
        :param String hostname: the name of the host
        :param nat port: port number to connect to
        :param Player player: the player that's playing over this
                              connection
        :param String playername: name of the player
        """
        self._player = PlayerGuard(player)
        self._player_name = player_name
        self._client_msger = ClientMessager(hostname, port)
        self._relay_state = RelayState.REGISTRATION
        self._our_uuid = uuid.uuid4()
        self._opp_uuid = uuid.uuid4()
        self._uuid_to_name = {self._our_uuid : player_name}
        self._player.set_id(self._our_uuid)

    def start(self):
        """
        Begin protocol.
        """
        # set relay state
        self._relay_state = RelayState.REGISTRATION
        # send name
        self._client_msger.send_register_message(self._player_name)

        while self._relay_state != RelayState.FINISHED:
            self.handle_message()

    def handle_message(self):
        """
        Receives a message from the server and handles it
        """
        message = self._client_msger.receive_message()

        if self._relay_state == RelayState.REGISTRATION and \
                validate_json(PLAYING_AS, message):
            _, new_name = message
            self.set_new_name(new_name)

        elif validate_json(OTHER, message):
            self.set_opp()
            self._relay_state = RelayState.PLACEMENT1

        elif validate_json(RESULTS, message):
            self._relay_state = RelayState.FINISHED

        elif (self._relay_state == RelayState.PLACEMENT1 or \
                self._relay_state == RelayState.TAKE_TURNS) and \
                validate_json(PLACEMENT, message):
            self._player.start_of_game()
            self.handle_placement(message)
            self._relay_state = RelayState.PLACEMENT2

        elif self._relay_state == RelayState.PLACEMENT2 and \
                validate_json(PLACEMENT, message):
            self.handle_placement(message)
            self._relay_state = RelayState.TAKE_TURNS

        elif self._relay_state == RelayState.TAKE_TURNS and \
                validate_json(BOARD, message):
            self.handle_take_turn(message)

        else:
            raise ValueError("got message: " + str(message) +
                             "in RelayState " + self._relay_state.name)

    def set_new_name(self, new_name):
        """
        set's a new name for this player
        :param String new_name: the player's new name
        """
        self._player_name = new_name
        self._uuid_to_name[self._our_uuid] = new_name

    def handle_placement(self, placement):
        """
        handles a placement request
        :param Json Placement placement: the placement request
        """
        workers = self.placement_to_workers(placement)
        self.enact_placement(workers)

    def handle_take_turn(self, board):
        """
        handles a take_turn request
        :param Json Board board: the board of the take_turn request
        """
        santorini_board = self.board_to_board(board)
        self.enact_turn(santorini_board)

    def set_opp(self):
        """
        Generate two uuids to represent this player and the opponent.
        This will be kept consistent for calls on this side of the
        connection and will be translated to player names when
        sending messages.
        Uuids will be kept track of in self._our_uuid and
        self._opp_uuid.
        The actual names of the players will be kept track of
        in self._uuid_to_name.
        """
        self._opp_uuid = uuid.uuid4()

    def enact_placement(self, workers):
        """
        Gets a placement from the player and sends it to the server.
        :param list(Worker) workers: the list of Workers already placed.
        """
        current_board = Board(workers=workers)
        placement = self._player.place_worker(current_board)
        self._client_msger.respond_placement_message(placement)

    def placement_to_workers(self, placement):
        """
        Converts Placement message to list of Workers.
        :param PlacementMsg placement: A list of [Worker, Coordinate, Coordinate]
        :rtype list(Workers): a list of Workers
        """
        workers = {}
        for workerplace in placement:
            worker, row, col = workerplace
            workers[self.worker_to_worker(worker)] = (row, col)
        return workers

    def worker_to_worker(self, worker):
        """
        Converts a string representation of a Worker to a worker.
        e.g. "potato2" would be a Worker of player "potato" and number 2
        :param WorkerMsg worker: a series of lowercase letters followed by either 1 or 2
        :rtype Worker worker: the Worker
        """
        player, number = worker[:-1], int(worker[-1:])
        player_uuid = self.name_to_uuid(player)
        return Worker(player_uuid, number)

    def name_to_uuid(self, name):
        """
        Get's a player's id from their name
        :param String name: name of convert to a Uuid
        """
        return self._our_uuid if self._player_name == name else self._opp_uuid

    def enact_turn(self, board):
        """
        Gets the player to play a turn and then sends it.
        :param Board board: the current board
        """
        turn = self._player.play_turn(board)
        self._client_msger.respond_turn_message(turn, self._our_uuid, self._uuid_to_name)

    def board_to_board(self, board_arr):
        """
        Converts a 2d Board cell array to a Board object
        :param [[Cell, ...], ...] board_arr: where Cell is either a Height (0, 1, 2, 3, 4)
                                             or a BuildingWorker, a Height followed by a Worker
        :rtype Board: a suitable board
        """
        new_board = [[0 for col in range(Board.BOARD_SIZE)] for row in
                     range(Board.BOARD_SIZE)]
        workers = {}
        for (row, rows) in enumerate(board_arr):
            for col in range(len(rows)):
                cur_cell = board_arr[row][col]
                if isinstance(cur_cell, int):
                    new_board[row][col] = cur_cell
                elif cur_cell:
                    new_board[row][col] = int(cur_cell[0])
                    worker_str = cur_cell[1:]
                    worker_num = int(worker_str[-1:])
                    player_name = worker_str[:-1]
                    cur_worker = Worker(self.name_to_uuid(player_name), worker_num)
                    if cur_worker:
                        workers[cur_worker] = (row, col)

        cur_board = Board(new_board, workers)
        return cur_board
