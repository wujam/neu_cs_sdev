import copy
"""
The Board class represents a 6x6 board, buildings and their heights, and
2 worker piece each for 2 players, for the Santorini game.
A high level process for using this class should be:
1. Initialize the Board
2. Set initial worker positions
3. Set worker positions/building heights as game progresses
4. Get data as game progresses
5. Query board to check if game is over
"""

"""
A Worker is (x,y) or None
  where x and y and are its x and y positions on the board
  x and y are integers where positive x represents east and
  positive y represents south
  
  A Worker is None if it is not set yet

A Building is an int that respresents it's height on the board

Building Heights on the board are in range [0,4]
  a 0 height Building has no floors built yet or equivalently is 'not a building'
  a 1-4 height Building is one with that many floors built
"""

class Board:
    # the length and width of the board
    BOARD_DIMENSION = 6
    # starting height of a Building
    BASE_BUILDING_HEIGHT = 0
    # highest height of a Building
    MAX_BUILDING_HEIGHT = 4

    # players is a list of 2 Players, with the first being designated Player 1 and
    # the second Player 2 in this documentation.
    # a Player is a list of two Workers, where the first of the list is considered
    # Worker 1 and the second is Worker 2
    players = None

    # a 6x6 2d list that containes Buildings
    squares = None

    """
    sets squares to 0 heights 
    """
    def __init__(self):
        self.squares = []
        self.players = [[None, None], [None, None]]
        for i in range(self.BOARD_DIMENSION):
            self.squares.append([self.BASE_BUILDING_HEIGHT] * self.BOARD_DIMENSION)

    """
    Sets the position of a worker
    x: the horizontal position of the worker to be placed, between [0,6)
    y: the vertical position of the worker to be placed, between [0,6)
    player: represents which player the worker belongs to, between [1,2]
    worker: represents which worker of the player is being placed, between [1,2]
    """
    def set_worker(self, x: int, y: int, player: int, worker: int):
       self.players[player - 1][worker - 1] = (x, y) 

    """
    Adds a floor to a Building.
    If the height at the specified Building is already at the max height,
    a ValueError will be raised.
    x: the horizontal position of the Building, between [0,6)
    y: the vertical position of the Building, between [0,6)
    raises ValueError: If the height at the specified Building is at maximum
    """
    def add_floor(self, x: int, y: int):
        self.set_floor_height(x, y, self.squares[x][y] + 1)

    """
    @return the number of floors in a Building
    x: the horizontal position of the Building, between [0,6)
    y: the vertical position of the Building, between [0,6)
    """
    def get_floor_height(self, x: int, y: int) -> int:
        return self.squares[x][y]

    """
    set the number of floors in a Building
    x: the horizontal position of the Building, between [0,6)
    y: the vertical position of the Building, between [0,6)
    height: the height to set the floor to, between [0,4]
    """
    def set_floor_height(self, x: int, y: int, height: int):
        self.squares[x][y] = height

    """
    @return the position of the specified worker, None if not set yet
    player: represents which player the worker belongs to, between [1,2]
    worker: represents which worker of the player is being placed, between [1,2]
    """
    def get_worker_position(self, player: int, worker: int) -> (int, int):
        return self.players[player - 1][worker - 1]        

    """
    Get a list of the positions of the game's workers.
    @return a list of Players in the order Player1, Player2
            each Player is a list of Workers in the order Worker1, Worker2
    """
    def get_worker_positions(self) -> []:
        return copy.deepcopy(self.players)

    """
    Get a 6x6 2d list of the Building heights. The outer list is the horizontal positions,
    and the inner list is the vertical positions.
    @return a 6x6 2d list of ints, the outer list representing rows, and the inner list representing
            cells or columns.
    """
    def get_building_heights(self) -> []:
        return copy.deepcopy(self.squares)
