"""
A Strategy object determines moves based on a game state.
"""
def Strategy:
    def __init__(self):
        pass

    """
    This function should give back the 'best' move to make with the given
    game state.
    @buildings: a 2d list of ints from [0-4]. The outer list is a list
                of columns, and the inner list is a list of heights
                representing the height of each building.
                The positive direction of the outer list represents
                "East" and the positive direction of the inner list
                represents "South".
    @players: a list of two Players, where the first member of the list is
              the player this class is representing, and the second is the
              opposing player. A Player is a list of Workers, which are
              tuples of two ints (x, y) representing their position on the board.
              The x and y directions are the same as the buildings'.
    @return: A tuple of (workernumber, direction_to_move, direction_to_build)
             A workernumber is an integer designating the Worker to be moved
             as its index in the given Workers list.
             A directiontomove is a tuple of two ints (x,y), each in the range
             [-1,1], but cannot be (0,0).
             A directiontobuild is a tuple of two ints (x,y) each in the range
             [-1,1]. Can be (0,0) only if the move is a winning move.
    """
    def get_move(self, buildings, players):
        pass

    """
    Get a worker placement from this strategy component given a game state.
    @players: a list of two Players, as defined above. The first Player
              in the list is a list of the workers this player is representing,
              and the second Player is a list of workers the opposing player is
              representing. These lists will not necessarily contain 2 workers,
              but the workers contained in both lists represent all the workers
              currently on the board.
    @return: A tuple of 2 ints (x,y) each from [0,5] representing the position
             that this strategy component chooses to place the next worker.
    """
    def get_worker_placement(self, players):
        pass
        