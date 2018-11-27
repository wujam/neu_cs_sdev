import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
import Santorini.Player.tree_strat
import Santorini.Player.place_strat
from Santorini.Common.player_interface import AbstractPlayer

class TemplatePlayer(AbstractPlayer):
    
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id

    def start_of_game(self):
        """Initialize the player.

        Called once at the start of the game to do any needed
        initializtion for the implementation of the player.
        """
        pass

    def set_name(self, name, new_name=False):
        pass

    def set_opponent(self, opp_id, name):
        pass

    def place_worker(self, cur_board):
        """Worker Placement.
        :param Board cur_board: a copy of the current board
        """
        place_strat.PlaceStratDiagonal.plan_placement(self._player_id, cur_board)

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        our_workers = [worker for worker in cur_board.workers() if worker.player == self._player_id]
        tree_strat.TreeStrategy.plan_turn(our_workers, cur_board)

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
        pass
