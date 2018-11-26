"""Takes in a socket connection handles messages"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from Santorini.Remote.jsonschemas import PLAYING_AS_STR
import json


class ServerMessager:
    def __init__(self, socket):
        """ Takes a connection to a client
        :param Socket, socket: the socket to communicate over
        """
        self._socket = socket

    def receive_message(self):
        """
        receives a message from the socket
        :rtype Json: the message received
        """
        message = self._socket.recv(4096).decode()
        return json.loads(message)

    def send_other_name(self, name):
        """
        sends an opponent's name to the client
        :param String name: opponent's name
        """
        self._send_json(name)

    def send_playing_as(self, name):
        """
        sends a new name to the client
        :param String name: new player name
        """
        self._send_json([PLAYING_AS_STR, name])

    def send_placement_request(self, placements):
        """
        sends a placement request to the client
        :param List of WorkerPlace placements: current worker placements
        """

        self._send_json(placements)

    def send_take_tun(self, board):
        """
        sends a take_turn request to the client
        :param Json Board board: current board state
        """

        self._send_json(board)

    def _send_json(self, json_msg):
        """
        sends a string of dumped json to the client
        :param Json json: json to be sent
        """
        json_dump = json.dumps(json_msg)
        self._socket.send(json_dump.encode())
