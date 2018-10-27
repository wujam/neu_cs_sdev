import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

class LoopPlayer():
    """ This player really likes loops. """
    
    def set_id(self, player_id):
        """Give a id for this Player.
        :param Uuid player_id, this player's uuid 
        """
        self._player_id = player_id
        while(True):
            pass

    def get_name(self):
        """Get a name to call this Player.
        :rtype String name, a name that this player wants to call itself.
        """
        while(True):
            pass
        return "templateplayer"

    def start_of_game(self):
        while(True):
            pass

    def place_worker(self, cur_board):
        """Worker Placement.
        :param Board cur_board: a copy of the current board
        """
        while(True):
            pass

    def play_turn(self, cur_board):
        """Regular Santorini turn.

        :param Board cur_board: a copy of the current state of the board
        :rtype Turn result_turn: the turn to be sent to the ref.
        """
        while(True):
            pass

    def game_over(self, winner):
        """Call when the game is over.

        If any of the endgame conditions are met (see is_gameover method
        in the rulechecker interface), this will be sent to the game
        to determine the winner of the game.

        The game will send back which player's name won the game based on
        endgame conditions and return this name to the player to compare to
        itself.

        :param str winner: the name of the Player that won the game
        """
        while(True):
            pass
