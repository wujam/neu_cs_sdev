import itertools
from functools import reduce
"""
A sub-strategy that determines the next move to make outside of the start up phase
"""
class TurnStrategy:
    WORKER_MOVE_DISTANCE = 1
    WORKER_HEIGHT_MOVE_DIFF = 1
    BOARD_SIZE = 6
    MAX_HEIGHT = 4
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
    def get_move(self, buildings, players, lookaheads):
    # List of tuples of (Turn, Turns)
    # A Turn is (WorkerNum, WorkerMoveDirection, BuildingMoveDirection)
        turn_tree = _get_node_generator(self, players, buildings) 
    


    """
    Gets a generator of all possible moves for the player from the given board position.
    @players: a list of two Players, where the first member of the list is
              the player this class is representing, and the second is the
              opposing player.
    @buildings: a list of list of heights. The outer list should be a list of columns,
                and the inner list should be a list of cells. The positive direction
                of the outer list should be considered "East" and the positive direction
                of the iner list should be considerd "South".
    @return: a generator of all possible legal moves (worker, move_direction, building_move_direction)
    """
    @staticmethod
    def _get_node_generator(players, buildings):
        our_workers = players[0]

        possible_worker_moves = iter(()) 

        for worker in our_workers:
            possible_worker_moves = itertools.chain(TurnStrategy._get_worker_moves(worker, players, buildings), possible_worker_moves) 

        possible_move_and_build_moves = iter(())
        for worker_move in possible_worker_moves:
            possible_move_and_build_moves = itertools.chain(TurnStrategy._get_possible_build_moves(worker_move[0], worker_move[1], players, buildings), possible_move_and_build_moves)

        return possible_move_and_build_moves

    @staticmethod
    def _get_worker_moves(worker, players, buildings):
        worker_height = TurnStrategy._get_height_at_position(buildings, worker[0], worker[1])
        all_workers = players[0] + players[1]
        for direction in TurnStrategy._gen_cardinal_directions():
            new_pos = TurnStrategy._add_tuples(worker, direction) 
            new_height = TurnStrategy._get_height_at_position(buildings, new_pos[0], new_pos[1])
            if (TurnStrategy._in_bounds(*new_pos) and
                new_pos not in all_workers and
                new_height - worker_height <= TurnStrategy.WORKER_HEIGHT_MOVE_DIFF):
                yield (worker, direction)
            else:
                continue

    @staticmethod
    def _get_possible_build_moves(worker, move_direction, players, buildings):
        all_workers = [w for w in players[0] if w is not worker] + [TurnStrategy._add_tuples(worker, move_direction)] + players[1]
        for direction in TurnStrategy._gen_cardinal_directions():
            build_pos = reduce(TurnStrategy._add_tuples, [worker, move_direction, direction], (0, 0))
            if (TurnStrategy._in_bounds(*build_pos) and
                build_pos not in all_workers and
                TurnStrategy._get_height_at_position(buildings, build_pos[0], build_pos[1]) < TurnStrategy.MAX_HEIGHT):
                yield (worker, move_direction, direction)
            else:
                continue

    @staticmethod
    def _gen_cardinal_directions():
        return itertools.product(range(0 - TurnStrategy.WORKER_MOVE_DISTANCE, 1 + TurnStrategy.WORKER_MOVE_DISTANCE),
                                 range(0 - TurnStrategy.WORKER_MOVE_DISTANCE, 1 + TurnStrategy.WORKER_MOVE_DISTANCE))

    @staticmethod
    def _get_height_at_position(buildings, x, y):
        return buildings[x][y]

    @staticmethod
    def _add_tuples(t1, t2):
        return t1[0] + t2[0], t1[1] + t2[1]

    @staticmethod
    def _in_bounds(x, y):
        return x in range(0, TurnStrategy.BOARD_SIZE) and y in range(0, TurnStrategy.BOARD_SIZE)
