import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from Santorini.Player.tree_strat import *
from Santorini.Player.place_strat import *

class MalformedDataPlayer:
    """ This player didn't read the data spec. """
    
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id

    def get_name(self):
        """Get a name to call this Player.
        :rtype String name, a name that this player wants to call itself.
        """
        #returns a tuple of each character from the string
        return tuple("malformed data player",)

    def start_of_game(self):
        pass

    def place_worker(self, cur_board):
        """Worker Placement.
        :param Board cur_board: a copy of the current board
        """
        placement = PlaceStratDiagonal.plan_placement(self._player_id, cur_board)
        return placement

    def play_turn(self, cur_board):
        """Regular Santorini turn.
        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        our_workers = [worker for worker in cur_board.workers if worker.player == self._player_id]
        return ("potato", "tomato", "foo")

    def end_of_game(self, winner):
        """
        :param str winner: the name of the Player that won the game
        """
        pass
