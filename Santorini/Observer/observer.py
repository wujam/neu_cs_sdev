sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import Board, Direction
import json

class Observer:
    """Interface for a Observer object in Santorini."""

    def __init__(self, referee):
        """Create an observer object that plugs into the referee
        
        The method should plug into the referee that it will observe
        in order to send and receive messages from it
        :param referee: the referee that this 
        """
        self.board = Board()

    def update_placement(self, board, placement, id_to_name)
        """Receives a placement and updates

        A placement is a tuple of worker and
        positon (in the form ( Worker, (row, col)),

        :param Board board: a copy of the current game board
        :param placement placement: a turn that the player inputted
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        print(self._dump_board(board, id_to_name))

    def update_turn(self, board, turn, id_to_name):
        """Receives a turn and updates.

        A turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param Board board: a copy of the current game board
        :param turn turn: a turn that the player inputted
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        print(self._dump_board(board, id_to_name))
        print(self._dump_turn(board, id_to_name))

    def update_game_over(self, board, player, id_to_name):
        """Same notifies the observer that the game is over as well.


        :param Board board: a copy of the current game board
        :param player string: name of the player that won
        :param Dict{uuid, str} id_to_name: dict mapping of player_id to a string of the player name
        """
        print(self._dump_board(board, id_to_name))
        print(player)

    def update_error_msg(self, msg):
        """Takes a string that represents an error message
        prints out when a player mis-behaves

        :param str msg: the message as a string
        """
        print(msg)

    def _dump_board(self, board, id_to_name):
        """
        Gives a string representation of the board in json.
        :param Board board: the board
        :param map{Uuid -> String} id_to_name: map of uuids to player name
        :rtype String: the json representation of the board
        """
        tiles = []
        for i in range(BOARD_SIZE):
            tiles[i] = []
            for j in range(BOARD_SIZE):
                tiles[i][j] = board.get_height(i, j, Direction.STAY) 
        
        for w in board.workers:
            row, col = board.worker_position(w) 
            tiles[row][col] = str(tiles)[row][col] + self._dump_worker(w, id_to_name) 
            
        return json.dumps(json.loads(tiles)) 

    def _dump_worker(self, worker, id_to_name):
        """
        Gives a string representation of a worker in json.
        :param Worker worker: a Worker
        :param map{Uuid -> String} id_to_name: map of uuids to player name
        :rtype String: the json representation of the worker
        """
        return str(id_to_name[w.player]) + str(w.number)
        
    def _dump_turn(self, turn, id_to_name):

        """
        Gives a string representation of a turn in json.
        :param turn turn: the turn of a worker
        :param map{Uuid -> String} id_to_name: map of uuids to player name
        """
        worker, move_dir, build_dir = turn
        worker_string = self._dump_worker(worker, id_to_name)
        move_dir_string = str(move_dir)
        build_dir_string = "," + str(build_dir) if build_dir is not None and build_dir.vector is not (0,0)
                            else ""
        return ("[" + self._dump_worker(worker, id_to_name) + ","
                + move_dir_string + build_dir_string + "]") 
