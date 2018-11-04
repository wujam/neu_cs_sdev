import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import Board, Direction
import json

class Observer:
    """Interface for a Observer object in Santorini."""

    def __init__(self):
        """Create an Observer object """
        pass

    def update_placement(self, board, placement, id_to_name):
        """Receives a placement and updates

        A placement is a tuple of worker and
        positon (in the form ( Worker, (row, col)),

        :param Board board: a copy of the current game board
        :param placement placement: a turn that the player inputted
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        print(json.dumps(board.dump_as_json(id_to_name)))

    def update_turn(self, board, turn, id_to_name):
        """Receives a turn and updates.

        A turn is one of:
        (None, None, None) - A give_up request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param Board board: a copy of the current game board
        :param Turn turn: a turn that the player inputted, cannot be a give up move (None, None, None)
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        print(json.dumps(board.dump_as_json(id_to_name)))
        print(self._dump_turn(turn, id_to_name))

    def update_gave_up(self, player_name):
        """Receives a player who is giving up
        :param String player_name: name of the player who gave up
        """
        print(json.dumps("Player gave up: " + player_name))

    def update_game_over(self, board, player_name, id_to_name):
        """Same notifies the observer that the game is over as well.


        :param Board board: a copy of the current game board
        :param String player_name: name of the player that won
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        print(json.dumps(board.dump_as_json(id_to_name)))
        print(json.dumps("Winner: " + player_name))

    def update_error_msg(self, msg):
        """Takes a string that represents an error message
        prints out when a player mis-behaves

        :param str msg: the message as a string
        """
        print(json.dumps(msg))

    def _dump_turn(self, turn, id_to_name):

        """
        Gives a string representation of a turn in json.
        :param turn turn: the turn of a worker
        :param map{Uuid -> String} id_to_name: map of uuids to player name
        """
        worker, move_dir, build_dir = turn
        turn_list = []
        turn_list.append(worker.dump_with_name(id_to_name))
        turn_list.extend(move_dir.string_values())
        if build_dir is not None:
            turn_list.extend(build_dir.string_values())
        return json.dumps(turn_list)
