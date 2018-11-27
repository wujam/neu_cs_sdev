import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import socket
import uuid
from Santorini.Common.pieces import *
from Santorini.Common.player_guard import *
from Santorini.Remote.client_messager import ClientMessager
from Santorini.Remote.jsonschemas import PLAYING_AS, NAME, PLACEMENT, RESULTS 
from Santorini.Lib.json_validate import validate_json

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

    def start(self):
        """
        Begin protocol.
        """
        # set their uuid
        self._our_uuid = uuid.uuid4()
        self._player.set_id(self._our_uuid)
        # send name
        self._client_msger.send_register_message(self._player_name) 
        # play game loop
        while(True):
            # make the uuids and the uuid map
            self.initialize_uuid_control()
            # receive first message 
            next_msg = self.client_msger.receive_message()
            # figure out if it's the optional playing-as message, if so
            # use that name
            if validate_json(PLAYING_AS, next_msg)
                self._player_name = next_msg[1]
                self._uuid_to_name[self._our_uuid] = self._player_name
                # receive another message because there must be an "other" message
                next_msg = self.client_msger.receive_message()

            # start the tournament play phase
            playing_tournament = True
            while(playing_tournament):
                # receive the "other" message and set the opponent's name
                self._opponent_name = next_msg
                self._uuid_to_name[self._opp_uuid] = self._opponent_name

                playing_series = True
                while(playing_series):
                    # do placement phase
                    for i in range(2):
                        next_msg = self.client_msger.receive_message()
                        workers = self.placement_to_workers(next_msg)
                        self.enact_placement(workers)
                    # do playing turns 
                    while(True):
                        # receive a message
                        next_msg = self.client_msger.receive_message()
                        if json_validate(NAME, next_msg):
                            # we received an "other" message" so break
                            playing_series = False
                            break
                        elif json_validate(PLACEMENT, next_msg):
                            break
                        elif json_validate(RESULTS, next_msg):
                            playing_series = False
                            playing_tournament = False
                            break
                        else:
                            current_board = self.board_to_board(next_msg)
                            self.enact_turn(current_board)


    def initialize_uuid_control(self):
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
        self._uuid_to_name = {}
        self._uuid_to_name[self._our_uuid] = self._player_name


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
        workers = []
        for workerplace in placement:
            workers += self.worker_to_worker(workerplace)
        return workers

    def worker_to_worker(self, worker):
        """
        Converts a string representation of a Worker to a worker.
        e.g. "potato2" would be a Worker of player "potato" and number 2
        :param WorkerMsg worker: a series of lowercase letters followed by either 1 or 2
        :rtype Worker worker: the Worker
        """
        player, number = worker[:-1], worker[-1:]
        player_uuid = self._our_uuid if self._player_name == player else self._opp_uuid
        return Worker(player_uuid, number - 1)

    def enact_turn(self, board):
        """
        Gets the player to play a turn and then sends it.
        :param Board board: the current board
        """
        turn = self._player.play_turn(board)
        self._client_msger.respond_turn_message(turn, self._player_name)

    def board_to_board(self, board_arr):
        """
        Converts a 2d Board cell array to a Board object
        :param [[Cell, ...], ...] board_arr: where Cell is either a Height (0, 1, 2, 3, 4)
                                             or a BuildingWorker, a Height followed by a Worker
        :rtype Board: a suitable board
        """
        workers = []
        new_board_arr = []
        for row in range(len(board_arr)):
            current_row = board_arr[row]
            new_row = []
            for col in range(len(current_row)):
                current_cell = current_row[col]
                if isinstance(current_cell, int):
                    new_row += current_cell
                else:
                    new_row += int(current_cell[0])
                    worker_str = current_cell[1:]
                    workers += self.worker_to_worker(worker_str)
            new_board_arr += new_row

        return Board(new_board_arr, workers)
