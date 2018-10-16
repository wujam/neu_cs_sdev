"""
The Player class represents a set of functions that represents actiona a player will be asked to take.

The Player should receieve calls when it is it's turn of play (it's turn to make an action) and be given
all of the information that it needs to make that action (a board).

A GameState is a Board.
A Board is an implementation of a Board interface documented in Design.
"""
class Player:
    """
    Initializes internal Player components.
    @game_admin: A GameAdmin object of the game this player is playing.
    """
    def __init__(self):
        pass

    """
    Method to allow a player to determine if the game is over.
    @return: True if the game is over, else False.
    """
    def game_over(self) -> bool:
        pass

    """
    Method to ask the Player for a worker placement.
    @board: the current board that represents the game state.
    #player_num: the player number they are with reference to the board, between [0, 1]
    @return: A tuple (x, y) that represents the posiiton on the board
             for a worker to be placed
    """
    def get_worker_placement(self, board, player_num):
        pass

    """
    Method to ask the Player for a game turn.
    @board: the current board the represents the game state.
    #player_num: the player number they are with reference to the board, between [0, 1]
    @return 
    """
    def get_move(self, board, player_num):
        pass
