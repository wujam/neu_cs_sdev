"""
A sub-strategy that determines the best placement to make during the start-up phase
"""
def DiagonalPlacementStrategy:
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
             The position chosen will be a free positoin on the x=y diagonal.
             Will return None if there are no free spaces on the diagonal.
    """
    def get_worker_placement(self, players):
        #flatten list
        workers = [worker for player in players for worker in player]

        return next(placement for placement in zip(range(6), range(6))
               if (placement not in workers), None)



        
