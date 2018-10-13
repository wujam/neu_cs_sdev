"""
A sub-strategy that determines the best placement to make during the start-up phase
"""
def Placement_Strategy:
    def __init__(self):
        pass

    """
    Get a worker placement from this placement_strategy component given a game state.
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
