import itertools
from board import Board
from rulechecker import RuleChecker
from functools import reduce

"""
A sub-strategy that determines the next move to make outside of the start up phase

A BuildingGrid is a 2d list of ints from [0-4]. The outer list is a list
    of columns, and the inner list is a list of heights representing
    the height of each building. The positive direction of the outer
    list represents "East" and the positive direction of the inner list
    represents "South".

A Player is a list of Workers, which are tuples of two ints
    (x, y) representing their position on the board.
    The x and y directions are in the same convention as the buildings'.
    No Workers in a Player can be in the same position as one another.
A PlayerList is a list of two Players.
    No Workers among all Players can be in the same position as one
    another.
A Turn is a tuple of (worker_number: int, move_direction: Direction,
    build_direction: Direction or (0,0))
    A worker_number is an integer designating the Worker to be moved
    as its index in the PlayerList.
    A Direction is a tuple of two ints (x,y), each in the range
    [-1,1], but cannot be (0,0).
    move_direction is a Direction
    build_direction is a Direction or (0,0) if the move is a winning move
A DeterminedTurn is a tuple of (worker_number: int, move_direction: Direction,
    build_direction: Direction or (0,0), win_move: bool)
    win_move is a bool that's True if the move is a move that wins, otherwise False
A PartialTurn is a tuple of (worker_number: int, move_direction: Direction)
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
    @buildings: A BuildingGrid that represents the board state
    @player: 0 or 1, the Player whose turn it is
    @players: A PlayerList where the first Player represents the player
              this class is representing, and the second player represents
              the opposing player.
    @lookaheads: Nat, number of turns to look ahead.
    @return: A DeterminedTurn that represents the best next turn, else None if all
             moves lead to loss.
    """
    def get_move(self, buildings, players, lookaheads):
        turn_tree = _get_node_generator(self, players, buildings) 
        current_board = Board(players, buildings)
        worker_index = player[0].index(worker)
        if lookaheads == 0:
            # find a non-dead move one layer deep
            viable_turns = []
            for worker, move_direction, build_direction in turn_tree:
                temp_board = Board(current_board)
                rulecheck = RuleChecker(temp_board)
                # move worker
                new_pos = TurnStrategy._add_tuples(worker, move_direction)
                build_pos = TurnStrategy._add_tuples(new_pos, build_direction)
                temp_board.set_worker(new_pos[0], new_pos[1], 0, worker_index)
                # build on building
                temp_board.add_floor(build_pos[0], build_pos[1])
                game_over = rulecheck.is_game_over()
                if game_over is not -1:
                    viable_turns.append((worker, move_direction, build_direction, False))
                elif game_over == 0:
                    # if we have a move that wins, return it
                    return (worker, move_direction, build_direction, True)
                else:
                    continue
            # if no moves don't lead to loss, return None, else return a safe move
            if len(viable_turns) == 0:
                return None
            return viable_turns[0]
        else:
            viable_turns = []

            for worker, move_direction, build_direction in turn_tree:
                next_opposing_move = self.get_move(buildings, players[1] + players[0], lookaheads - 1)
                if next_opposing_move is None:
                    return (worker, move_direction, build_direction, True)
                elif next_opposing_move[3]:
                    continue
                else:
                    viable_turns.append((worker, move_direction, build_direction, False))

            if len(viable_turns) == 0:
                return None
            return viable_turns[0]

    """
    Gets a generator of all possible turns for the player from the given board position.
    @players: A PlayerList where the first member of the list is
              the player this class is representing, and the second is the
              opposing player.
    @buildings: A BuildingGrid that represents the board state 
    @return: a generator of all possible legal Turns
    """
    @staticmethod
    def _get_node_generator(players, buildings):
        our_workers = players[0]
        possible_worker_moves = iter(()) 

        for worker in our_workers:
            possible_worker_moves = itertools.chain(TurnStrategy._get_worker_moves(worker, players, buildings), possible_worker_moves) 

        possible_move_and_build_moves = iter(())
        for worker_move in possible_worker_moves:
            possible_move_and_build_moves = itertools.chain(TurnStrategy._get_possible_build_moves(worker_move[0], worker_move[1], players, buildings),
                                                            possible_move_and_build_moves)

        return possible_move_and_build_moves

    """
    Gets a generator of all possible moves for a given worker.
    @worker: the Worker to determine all possible moves for
    @players: A PlayerList where the first member of the list is
              the player this class is representing, and the second is the
              opposing player.
    @buildings: A BuildingGrid that represents the board state 
    """
    @staticmethod
    def _get_worker_moves(worker, players, buildings):
        worker_index = players[0].index(worker)
        worker_height = buildings[worker[0]][worker[1]]
        all_workers = players[0] + players[1]
        cur_board = Board(players, buildings)
        for direction in TurnStrategy._gen_cardinal_directions():
            new_pos = TurnStrategy._add_tuples(worker, direction) 
            new_height = buildings[new_pos[0]][new_pos[1]]
            """
            if (TurnStrategy._in_bounds(*new_pos) and
                new_pos not in all_workers and
                new_height - worker_height <= TurnStrategy.WORKER_HEIGHT_MOVE_DIFF):
            """
            rulecheck = RuleChecker(cur_board)
            if (rulecheck.is_move_valid(0, worker_index, direction) or
                direction is (0,0)):
                yield (worker, direction)
            else:
                continue

    """
    Gets a generator of all possible turns for a worker for a given move.
    @worker: the Worker to determine all possible moves for
    @move_direction: a Direction to move in
    @players: A PlayerList where the first member of the list is
              the player this class is representing, and the second is the
              opposing player.
    @buildings: A BuildingGrid that represents the board state 
    @return: a generator of all possible Turns
    """
    @staticmethod
    def _get_possible_build_moves(worker, move_direction, players, buildings):
        worker_index = players[0].index(worker)
        all_workers = [w for w in players[0] if w is not worker] + [TurnStrategy._add_tuples(worker, move_direction)] + players[1]
        cur_board = Board(players, buildings)
        rulecheck = RuleChecker(cur_board)

        # check if the game is over
        game_over = rulecheck.is_game_over()
        if game_over is not -1:
            if game_over == 0:
                # if its this player's win, return the winning move
                yield (worker, move_direction, (0,0))
            else:
                # if its the opponent's win, they've won, no moves are good
                # shouldn't reach here
                return

        for direction in TurnStrategy._gen_cardinal_directions():
            """
            build_pos = reduce(TurnStrategy._add_tuples, [worker, move_direction, direction], (0, 0))
            if (TurnStrategy._in_bounds(*build_pos) and
                build_pos not in all_workers and
                buildings[build_pos[0]][build_pos[1]] < TurnStrategy.MAX_HEIGHT):
            """
            valid_move =  rulecheck.is_move_and_build_valid(0, worker_index, move_direction, direction)
            if valid_move:
                yield (worker, move_direction, direction)
            

    """
    @return: a list of all possible Directions and (0,0)
    """
    @staticmethod
    def _gen_cardinal_directions():
        return itertools.product(range(0 - TurnStrategy.WORKER_MOVE_DISTANCE,
                                        1 + TurnStrategy.WORKER_MOVE_DISTANCE),
                                 range(0 - TurnStrategy.WORKER_MOVE_DISTANCE,
                                        1 + TurnStrategy.WORKER_MOVE_DISTANCE))

    """
    convenience method to add two tuples of size 2 together
    @t1: a tuple of (Number, Number)
    @t2: a tuple of (Number, Number)
    @return: a tuple of (Number, Number)
    """
    @staticmethod
    def _add_tuples(t1, t2):
        return t1[0] + t2[0], t1[1] + t2[1]

    """
    convenience method to bounds check x and y values to make sure
    they're within the board
    @x: an Int
    @y: an Int
    @return: a boolean True if the given x and y are on the board, else False
    """
    @staticmethod
    def _in_bounds(x, y):
        return x in range(0, TurnStrategy.BOARD_SIZE) and y in range(0, TurnStrategy.BOARD_SIZE)
