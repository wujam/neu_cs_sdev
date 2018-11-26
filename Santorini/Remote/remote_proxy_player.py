import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.player_interface import AbstractPlayer
import Santorini.Common.rulechecker


class RemoteProxyPlayer(AbstractPlayer):
    """ Communicates with a player across the network."""

    def __init__(self, socket, timeout=5):
        """ Create a Player.
        :param Socket socket: The Socket to send messages to and listen for messages from.
        """
        self._socket = socket

    def set_id(self, player_id):
        """ Send a set id message to the remote Player.
        
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id
        self._send_set_id_message(player_id)

    def place_worker(self, cur_board):
        """Worker Placement.

        :param Board cur_board: a copy of the current board
        :rtype tuple (Worker, (row, col)) placement: the placement
        """
        return self._send_place_worker(cur_board)

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        return self._send_play_turn(cur_board)

    def start_of_game(self):
        """Initialize the player.

        Called once at the start of the game to do any needed
        initialization for the implementation of the player.
        
        For the implementation of the Assignment 13 network spec,
        this will not do anything
        """
        pass
    def end_of_game(self, won):
        """Call when the game is over.

        For the implementation of the Assignment 13 network spec,
        this will not do anything.
        :param str winner: the name of the Player that won the game
        """
        pass
