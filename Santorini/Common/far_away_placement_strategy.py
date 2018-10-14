import math
"""
A sub-strategy that determines the best placement to make during the start-up phase
"""
class FarAwayPlacementStrategy:
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
        # get worker lists, remove workers that don't exist
        our_workers = [worker for worker in players[0] if worker is not None]
        opp_workers = [worker for worker in players[1] if worker is not None]

        # return (0,0) if there aren't any opponent workers
        if (all(worker is None for worker in opp_workers)):
            return (0,0)

        max_dist_posn = (0,0)
        max_dist = 0

        # get distance between every possible posn on the board and
        # choose the one with the greatest distance
        for i in range(6):
            for j in range(6):
                # don't pick a position where a worker is already
                if ((i, j) in our_workers or (i, j) in opp_workers):
                    continue

                dist = 0

                # calculate distance between both workers
                for worker in opp_workers:
                    dist += self._dist_between_points(worker, (i, j))

                # pick this point if it's at the maximum distance so far
                if (dist > max_dist):
                    max_dist_posn = (i, j)
                    max_dist = dist

        return max_dist_posn

    """
    Get the euclidian distance between two positions
    @posn1, posn2: a tuples of 2 ints(x,y) each from [0,5] representing the
                   positions of the points to calculate the distance of
    @returns a number representing the euclidian distance between two points
    """
    def _dist_between_points(self, posn1, posn2):
        return math.sqrt((posn1[0] - posn2[0]) ** 2 + (posn1[1] - posn2[1]) ** 2)
