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
A worker is (x,y) or None
  where x and y and are its x and y positions on the board
  x and y are integers where positive x represents east and
  positive y represents south
  
  A workeer is None if it is not set yet

A building is an int that respresents it's height on the board

Building Heights on the board are in range [0,4]
  a 0 height building has no floors built yet or equivalently is 'not a building'
  a 1-4 height building is one with that many floors built
"""

class Board:
    # the length and width of the board
    BOARD_DIMENSION = 6

    # starting height of a building
    BASE_BUILDING_HEIGHT = 0

    # highest height of a builing
    MAX_BUILDING_HEIGHT = 4

    # worker objects that contain a tuple of the x and y position on the board
    p1worker1 = None
    p1worker2 = None
    p2worker1 = None
    p2worker2 = None

    # a 6x6 2d list that containes buildings
    squares = None

    """
    sets squares to 0 heights 
    """
    def __init__(self):
        self.squares = []
        for i in range(self.BOARD_DIMENSION):
            self.squares.append([self.BASE_BUILDING_HEIGHT] * self.BOARD_DIMENSION)

    """
    Sets the position of a worker
    x: the horizontal position of the worker to be placed, between [0,6)
    y: the vertical position of the worker to be placed, between [0,6)
    player: represents which player the worker belongs to, between [0,2)
    worker: represents which worker of the player is being placed, between [0,2)
    """
    def set_worker(self, x: int, y: int, player: int, worker: int):
        if player == 1 and worker == 1:
            self.p1worker1 = (x, y)
        elif player == 1 and worker == 2:
            self.p1worker2 = (x, y)
        elif player == 2 and worker == 1:
            self.p2worker1 = (x, y)
        elif player == 2 and worker == 2:
            self.p2worker2 = (x, y)
        else:
            raise ValueError(f"Player {player} and/or Worker {worker} out of range")

    """
    Adds a floor to a building
    x: the horizontal position of the building, between [0,6)
    y: the vertical position of the building, between [0,6)
    """
    def add_floor(self, x: int, y: int):
        if self.squares[x][y] == self.MAX_BUILDING_HEIGHT:
            raise ValueError(f"Building at {x}, {y} cannot be added to")
        self.squares[x][y] = self.squares[x][y] + 1

    """
    @return the number of floors in a building
    x: the horizontal position of the building, between [0,6)
    y: the vertical position of the building, between [0,6)
    """
    def get_floor_height(self, x: int, y: int) -> int:
        return self.squares[x][y]

    """
    set the number of floors in a building
    x: the horizontal position of the building, between [0,6)
    y: the vertical position of the building, between [0,6)
    height: the height to set the floor to
    """
    def set_floor_height(self, x: int, y: int, height: int) -> int:
        # have to add 1 to the python range function here because it is not inclusive
        # on the upper bound
        if height not in range(self.BASE_BUILDING_HEIGHT, self.MAX_BUILDING_HEIGHT + 1):
            raise ValueError(f"Building at {x}, {y} cannot be set to {height}")
        self.squares[x][y] = height

    """
    @return the position of the specified worker, None if not set yet
    player: represents which player the worker belongs to, between [0,2)
    worker: represents which worker of the player is being placed, between [0,2)
    """
    def get_worker_position(self, player: int, worker: int) -> (int, int):
        if player == 1 and worker == 1:
            return self.p1worker1
        elif player == 1 and worker == 2:
            return self.p1worker2
        elif player == 2 and worker == 1:
            return self.p2worker1
        elif player == 2 and worker == 2:
            return self.p2worker2
        else:
            raise ValueError(f"Player {player} and/or Worker {worker} out of range")

    """
    Get a list of the positions of the game's workers.
    @return a list of tuples representing the position of workers or None if worker isn't set.
            The exact ordering is P1 Worker 1, P1 Worker 2, P2 Worker 1, P2 worker 2.
    """
    def get_worker_positions(self) -> []:
        return [self.p1worker1, self.p1worker2, self.p2worker1, self.p2worker2]

    """
    Get a 6x6 2d list of the building heights. The outer list is the horizontal positions,
    and the inner list is the vertical positions.
    @return a 6x6 2d list of ints, the outer list representing rows, and the inner list representing
            cells or columns.
    """
    def get_building_heights(self) -> []:
        return copy.deepcopy(self.squares)
