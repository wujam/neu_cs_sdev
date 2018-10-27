import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import Santorini.Player.tree_strat
import Santorini.Player.place_strat
import Santorini.Common.pieces

class LegitPlayer():
    """ This player is legit. It plays by the rules. """
    
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id
        self._worker_count = 0

    def get_name(self):
        """Get a name to call this Player.
        :rtype String name, a name that this player wants to call itself.
        """
        return "legit player"

    def start_of_game(self):
        pass

    def place_worker(self, cur_board):
        """Worker Placement.
        :param Board cur_board: a copy of the current board
        """
        placement = place_strat.PlaceStratDiagonal.plan_placement(self._player_id, cur_board)
        self._worker_count = self._worker_count + 1
        worker = pieces.Worker(self._player_id, self._worker_count)
        return (worker, placement)

    def play_turn(self, cur_board):
        """Regular Santorini turn.
        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        our_workers = [worker for worker in cur_board.workers() if worker.player == self._player_id]
        return tree_strat.TreeStrategy.plan_turn(our_workers, cur_board)

    def game_over(self, winner):
        """
        :param str winner: the name of the Player that won the game
        """
        pass
