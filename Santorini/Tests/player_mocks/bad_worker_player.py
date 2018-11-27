import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from Santorini.Player.tree_strat import *
from Santorini.Player.place_strat import *
from Santorini.Common.pieces import *
from Santorini.Common.player_interface import AbstractPlayer
import uuid

class BadWorkerPlayer(AbstractPlayer):
    """ This player does well formed worker placements with workers that don't belong to him. """
    
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id
        self._worker_count = 0

    def start_of_game(self):
        pass

    def set_name(self, name, new_name=False):
        pass

    def set_opponent(self, opp_id, name):
        pass

    def place_worker(self, cur_board):
        """Worker Placement.
        :param Board cur_board: a copy of the current board
        """
        placement = PlaceStratDiagonal.plan_placement(self._player_id, cur_board)
        self._worker_count = self._worker_count + 1
        worker = Worker(uuid.uuid4(), self._worker_count)
        return (worker, placement)

    def play_turn(self, cur_board):
        """Regular Santorini turn.
        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        our_workers = [worker for worker in cur_board.workers() if worker.player == self._player_id]
        return TreeStrategy.plan_turn(our_workers, cur_board)

    def end_of_game(self, winner):
        """
        :param str winner: the name of the Player that won the game
        """
        pass
