import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import json
from Santorini.Common.player_interface import AbstractPlayer
from Santorini.Common.pieces import Worker, DIR_TABLE
from Santorini.Remote.jsonschemas import PLAYING_AS_STR, PLACE, ACTION
from Santorini.Lib.json_validate import validate_json


class RemoteProxyPlayer(AbstractPlayer):
    """ Communicates with a player across the network."""

    def __init__(self, socket):
        """ Create a Player.
        :param Socket socket: The Socket to send messages to and listen for messages from.
        """
        self._socket = socket
        self._uuid_to_name = {}

    def set_id(self, player_id):
        """ Sets id of the player internally

        :param Uuid player_id: this player's uuid
        """
        self._player_id = player_id

    def set_name(self, name, new_name=False):
        """ Send a set name message to the remote Player

        :param String name: this player's name
        """
        self._uuid_to_name[self._player_id] = name
        if new_name:
            self._send_json([PLAYING_AS_STR, name])

    def set_opponent(self, opp_id, name):
        """ Set the opponent and send it to the remote Player

        :param Uuid opp_id: opponent's id
        :param String name: opponent's name
        """
        self._uuid_to_name[opp_id] = name

        self._send_json(name)

    def place_worker(self, cur_board):
        """ask the client for a placement given the current placements

        :param Board cur_board: a copy of the current board
        :rtype tuple (Worker, (row, col)) placement: the placement
        """
        self._worker_count += 1
        worker_placements = cur_board.dump_workers_as_json(self._uuid_to_name)

        self._send_json(worker_placements)
        place = self._recv_json()
        if not validate_json(PLACE, place):
            raise ValueError("place didn't validate: " + str(place))

        worker = Worker(self._player_id, self._worker_count)

        return (worker, tuple(place))

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        board_json = cur_board.dump_as_json(self._uuid_to_name)

        self._send_json(board_json)
        action = self._recv_json()

        if not validate_json(ACTION, action):
            raise ValueError("action didn't validate: " + str(action))

        # make Turn from action
        if isinstance(action, str):
            if action == self._uuid_to_name[self._player_id]:
                return (None, None, None)
            else:
                raise ValueError("malicious give up action")
        else:
            return self._non_giveup_action_to_turn(action, cur_board)

    def _non_giveup_action_to_turn(self, action, cur_board):
        """ converts a non give up action to a Turn
        :param Action action: An action that isn't a give up action
        :param Board cur_board: a copy of the current state of the board
        :rtype Turn
        """
        worker_str = action[0]
        move_ew = action[1]
        move_ns = action[2]
        player_name = worker_str[:-1]
        if player_name != self._uuid_to_name[self._player_id]:
            raise ValueError("malicious player name in worker")
        worker_num = int(worker_str[-1])
        worker = None
        for w in cur_board.workers:
            if w.player == self._player_id and w.number == worker_num:
                worker = w
        move_dir = DIR_TABLE[(move_ew, move_ns)]
        if len(action) == 3:
            return (worker, move_dir, None)
        else:
            build_ew = action[3]
            build_ns = action[4]
            build_dir = DIR_TABLE[(build_ew, build_ns)]
            return (worker, move_dir, build_dir)

    def start_of_game(self):
        """Initialize the player.

        Called once at the start of the game to do any needed
        initialization for the implementation of the player.
        
        For the implementation of the Assignment 13 network spec,
        this will not do anything
        """
        self._worker_count = 0

    def end_of_game(self, won):
        """Call when the game is over.

        For the implementation of the Assignment 13 network spec,
        this will not do anything.
        :param str winner: the name of the Player that won the game
        """
        pass

    def _recv_json(self):
        message = self._socket.recv(4096).decode()
        return json.loads(message)

    def _send_json(self, json_msg):
        """
        sends a string of dumped json to the client
        :param Json json: json to be sent
        """
        json_dump = json.dumps(json_msg)
        self._socket.send(json_dump.encode())
