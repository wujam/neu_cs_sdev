"""
The Board class represents a 6x6 board, buildings and their heights, and
2 worker piece each for 2 players, for the Santorini game.
A high level process for using this class should be:
1. Initialize the Board
2. Set initial worker positions
3. Set worker positions/building heights as game progresses
4. Get data as game progresses
"""
class Board:
    # worker objects that contain a tuple of the x and y position on the board
    p1worker1 = None
    p1worker2 = None
    p2worker1 = None
    p2worker2 = None

    # a 6x6 2d list that containes buildings
    squares = []

    """
    sets squares to Building objects
    """
    def __init__ ():
        pass

    """
    Sets the position of a worker
    x: the horizontal position of the worker to be placed, between [0,6)
    y: the vertical position of the worker to be placed, between [0,6)
    player: represents which player the worker belongs to, between [0,2)
    worker: represents which worker of the player is being placed, between [0,2)
    """
    def set_worker(x: int, y: int, player: int, worker: int):
        pass

    """
    Adds a floor to a building
    x: the horizontal position of the building, between [0,6)
    y: the vertical position of the building, between [0,6)
    """
    def add_floor(x: int, y: int):
        pass

    """
    @return the number of floors in a building
    x: the horizontal position of the building, between [0,6)
    y: the vertical position of the building, between [0,6)
    """
    def get_floor_height(x: int, y: int) -> int:
        pass

    """
    @return the position of the specified worker
    player: represents which player the worker belongs to, between [0,2)
    worker: represents which worker of the player is being placed, between [0,2)
    """
    def get_worker_position(player: int, worker: int) -> (int, int):
        pass

    """
    Get a list of the positions of the game's workers.
    @return a list of tuples representing the position of workers.
            The exact ordering is P1 Worker 1, P1 Worker 2, P2 Worker 1, P2 worker 2.
    """
    def get_worker_positions() -> []:
        pass

    """
    Get a 6x6 2d list of the building heights. The outer list is the horizontal positions,
    and the inner list is the vertical positions.
    @return a 6x6 2d list of ints, the outer list representing rows, and the inner list representing
            cells or columns.
    """
    def get_building_heights() -> []:
        pass
