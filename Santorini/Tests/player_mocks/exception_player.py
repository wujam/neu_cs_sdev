"""Player implementation in Santorini"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from Santorini.Design.player import AbstractPlayer
import Santorini.Common.rulechecker
from Santorini.Common.pieces import Worker
from Santorini.Player.strategy import Strategy
from Santorini.Player.place_strat import PlaceStratDiagonal
from Santorini.Player.tree_strat import TreeStrategy

class Player(AbstractPlayer):
    """Player data reprensation in Santorini."""

    def __init__(self, name):
        """Create a Player.

        :param str name: the user's input name for the game
        :param AbstractStrategy strategy: any strategy object
        """
        raise Exception("derp")

    def start_of_game(self):
        """Initialize the player.

        Called once at the start of the game to do any needed
        initialization for the implementation of the player.
        """
        raise Exception("derp")

    def place_worker(self, cur_board):
        """Worker Placement.

        :param Board cur_board: a copy of the current board
        """
        raise Exception("derp")

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        """
        raise Exception("derp")

    def game_over(self, won):
        """Call when the game is over.

        :param str winner: the name of the Player that won the game
        """
        raise Exception("derp")
