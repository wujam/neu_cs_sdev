"""Player implementation in Santorini"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Design.player import AbstractPlayer
import Santorini.Common.rulechecker
from Santorini.Common.pieces import Worker
from Santorini.Player.strategy import Strategy
from Santorini.Player.place_strat import PlaceStratDiagonal
from Santorini.Player.tree_strat import TreeStrategy

class Player(AbstractPlayer):
    """Player data reprensation in Santorini."""

    def __init__(self):
        """Create a Player.
        """
        self.strategy = Strategy(PlaceStratDiagonal(), TreeStrategy())
        self.workers = []

    def set_id(self, player_id):
        """Give a id for this Player.
        
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id


    def start_of_game(self):
        """Initialize the player.

        Called once at the start of the game to do any needed
        initialization for the implementation of the player.
        """
        pass

    def place_worker(self, cur_board):
        """Worker Placement.

        :param Board cur_board: a copy of the current board
        :rtype tuple (Worker, (row, col)) placement: the placement
        """
        new_worker = Worker(self, len(self.workers) + 1)
        self.workers.append(new_worker)
        placement = self.strategy.plan_placement(new_worker, cur_board)
        return new_worker, placement

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        return self.strategy.plan_turn(self.workers, cur_board)

    def game_over(self, won):
        """Call when the game is over.

        :param str winner: the name of the Player that won the game
        """
        pass
