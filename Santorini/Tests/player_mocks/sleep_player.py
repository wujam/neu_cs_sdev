import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
import Santorini.Player.tree_strat
import Santorini.Player.place_strat
import Santorini.Common.pieces
import time
from Santorini.Common.player_interface import AbstractPlayer

class SleepPlayer(AbstractPlayer):
    """ This player really likes to sleep. """
    
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id
        time.sleep(999999)

    def get_name(self):
        """Get a name to call this Player.
        :rtype String name, a name that this player wants to call itself.
        """
        time.sleep(999999)
        return "sleep player"

    def start_of_game(self):
        time.sleep(999999)

    def place_worker(self, cur_board):
        """Worker Placement.
        :param Board cur_board: a copy of the current board
        """
        time.sleep(999999)
        placement = place_strat.PlaceStratDiagonal.plan_placement(self._player_id, cur_board)
        self._worker_count = self._worker_count + 1
        worker = pieces.Worker(self._player_id, self._worker_count)
        return (worker, placement)

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        time.sleep(999999)
        our_workers = [worker for worker in cur_board.workers() if worker.player == self._player_id]
        return tree_strat.TreeStrategy.plan_turn(our_workers, cur_board)

    def end_of_game(self, winner):
        """Call when the game is over.

        If any of the endgame conditions are met (see is_gameover method
        in the rulechecker interface), this will be sent to the game
        to determine the winner of the game.

        The game will send back which player's name won the game based on
        endgame conditions and return this name to the player to compare to
        itself.

        :param str winner: the name of the Player that won the game
        """
        time.sleep(999999)
