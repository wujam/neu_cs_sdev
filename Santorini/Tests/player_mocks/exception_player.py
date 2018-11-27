import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
import Santorini.Player.tree_strat
import Santorini.Player.place_strat
from Santorini.Common.player_interface import AbstractPlayer

class ExceptionPlayer(AbstractPlayer):
    """ This player really really like exceptions. """
    
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id
        
        raise Exception(str(player_id))

    def start_of_game(self):
        raise Exception("foo")

    def set_name(self, name, new_name=False):
        pass

    def set_opponent(self, opp_id, name):
        pass

    def place_worker(self, cur_board):
        """Worker Placement.
        :param Board cur_board: a copy of the current board
        """
        placement = place_strat.PlaceStratDiagonal.plan_placement(self._player_id, cur_board)
        raise Exception(str(placement))

    def play_turn(self, cur_board):
        """Regular Santorini turn.
        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        our_workers = [worker for worker in cur_board.workers() if worker.player == self._player_id]
        placement = tree_strat.TreeStrategy.plan_turn(our_workers, cur_board)
        raise Exception(str(placement[0]) + str(placement[1]) + str(placement[2]))

    def end_of_game(self, winner):
        """
        :param str winner: the name of the Player that won the game
        """
        raise Exception("winner is " + str(self._player_id))
