"""
The Player class represents a set of functions that will take actions that a player is able to take.
The Player class will pass messages to the Administrator for actions like getting the board state, setting workers, and
taking moves, and the Administrator will validate moves and then do them if they're valid and it is the Player's turn.

A GameState is a tuple of [Board, Workers].
A Board is a 6x6 2d list of integers from [0,4] representing building heights.
The outer list contains the columns, and the inner list contains the cells in each column.
The positive x direction is "east", and the positive y direction is "south".
A Workers is a list of 4 tuples of two integers in the order [Player1-Worker1, Player1-Worker2, Player2-Worker1, Player2-Worker2],
where "Player1" is always considered this Player, so the first two workers are owned by the player represented by the current class.

"""
class Player:
    """
    Initializes internal Player components.
    @game_admin: A GameAdmin object of the game this player is playing.
    """
    def __init__(self, game_admin):
        pass
    """
    Method to get the current game state.
    @return: a GameState representing the current game's state.
    """
    def get_game_state(self):
        pass

    """
    Method to allow a player to determine their player number.
    @return: a number that's either 1 or 2 representing which player number the player is.
    """
    def get_player_number(self) -> int:
        pass

    """
    Method to allow a player to determine if it's their turn. 
    @return: True if it's this Player's turn, else False.
    """
    def get_turn(self) -> bool:
        pass

    """
    Method to allow a player to determine if the game is over.
    @return: True if the game is over, else False.
    """
    def is_game_over(self) -> bool:
        pass

    """
    Method to tell the game to set a worker in the initial setup of the game.
    @worker: the worker number of the worker to set
    @x: the horizontal position of the worker to set, positive x is "east".
    @y: the vertical position of the worker to set, positive y is "south".
    @return: True if the game is over, else False.
    """
    def set_worker(self, worker, x, y):
        pass

    """
    Method to take a turn, which consists of moving a worker and building a floor.
    @worker: the worker number of the worker to set
    @direction_to_move: tuple of an int within [-1, 1] and [-1, 1]. The first number specifies the x direction to move,
                        and the second number represents the y direction to move. Positive x is east, positive y is south.
                        cannot be (0, 0)
    @direction_to_build: tuple of an int within [-1, 1] and [-1, 1]. The numbers specify the direction to build relative
                         to the new position of the worker. If the move is game winning, this should be specified as (0,0).
                         cannot be (0, 0)
    """
    def move_worker_and_build(self, worker_number, direction_to_move, direction_to_build):
        pass

    """
    Method to check if a move is valid.
    @worker: the worker number of the worker to set
    @direction_to_move: tuple of an int within [-1, 1] and [-1, 1]. The first number specifies the x direction to move,
                        and the second number represents the y direction to move. Positive x is east, positive y is south.
    @direction_to_build: tuple of an int within [-1, 1] and [-1, 1]. The numbers specify the direction to build relative
                         to the new position of the worker. If the move is game winning, this should be specified as (0,0).
    @return: True if the move is valid
    """
    def is_move_valid(self, worker_number, direction_to_move, direction_to_build) -> bool:
        pass
