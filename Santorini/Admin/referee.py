#!/usr/bin/python3.6
"""Implementation of the referee in Santorini."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import Board, Worker
from Santorini.Common import rulechecker
from Santorini.Admin.player_guard import *
from Santorini.Admin.observermanager import ObserverManager
import itertools
import copy
from enum import Enum
import logging
logging.basicConfig(filename='refereetest.log', filemode='w')

class PlayerResult(Enum):
    OK = 0
    GIVE_UP = 1
    BAD = 2
    NEFARIOUS = 3
class Referee:

    """Implementation of the Referee component in Santorini."""
    NUM_PLAYERS = 2
    NO_WINNER = -1

    def __init__(self, uuids_players, timeout=30):
        """Create a referee component with the associated list of players.
        :param dict[UUID -> Player] uuid_player: dictionary of UUIDs to players
        :param int timeout: the timeout in seconds for untrusted code (Players and Observers)
        """
        self.players = []
        self.timeout = timeout
        self.uuids_to_player = {}
        self.uuids_to_name = {}
        for uuid, player in uuids_players.items():
            player_guard = PlayerGuard(player, timeout=self.timeout)
            self.uuids_to_player[uuid] = player_guard
            self.players.append(player_guard)
        self.observer_manager = ObserverManager()

    def run_game(self):
        """Supervise a game between players.
        :rtype tuple(PlayerResult.OK, Uuid) the player won the game
               tuple(PlayerResult.NEFARIOUS, list(Uuid))
                   these players did something untrustworthy in
                   order of their appearance in the list
        """
        result = self._initialize()

        if result is PlayerResult.OK:
            player_ids = self.uuids_to_player.keys()
            result, player = self._play_game(player_ids)
            winner, evil_players = self._determine_winner_result((result, player))
        else:
            winner, evil_players = self._determine_init_result(result)

        return self._end_game(winner, evil_players)

    def run_n_games(self, num_games):
        """Supervises a best of num_games game series with the two players

        Will call run_game num_games times and tally up the score

        :param int num_games: the number of games to play in this series
                              this should be an odd number
        :rtype tuple(PlayerResult.OK, Uuid) the player won the series
               tuple(PlayerResult.NEFARIOUS, list(Uuid))
                   these players did something untrustworthy in
                   order of their appearance in the list
        """

        player_scores = [0, 0]

        init_result = self._initialize()
        evil_players = []
        player_ids = [p_id for p_id in self.uuids_to_player]

        if init_result is PlayerResult.OK:
            # run the series
            for i in range(num_games):
                self._reset_board()
                player_order = player_ids if i % 2 == 0 else [i for i in reversed(player_ids)]
                result, player = self._play_game(player_order)
                winner, evil_players = self._determine_winner_result((result, player))

                endresult, evil_players = self._end_game(winner, evil_players)
                if endresult is PlayerResult.NEFARIOUS:
                    break
                player_scores[player_ids.index(winner)] += 1

            # end the series
            if len(evil_players) > 0:
                # if we encountered any bad players, notify manager
                return (PlayerResult.NEFARIOUS, evil_players)
            else:
                # else give back the winner
                max_score = max(player_scores)
                index_of_winner = player_score.index(max_score)

                overall_winner = player_ids[index_of_winner]
                return (PlayerResult.OK, overall_winner)

        else:
            winner, evil_players = self._determine_init_result(init_result)
            endresult, evil_players = self._end_game(winner, evil_players)
            return (PlayerResult.NEFARIOUS, evil_players)

    def set_turn_timeout(self, timeout):
        """Sets a the turn timeout in seconds
        :param int timeout: Positive integer number of seconds. Players
                            who take longer than this to take an action
                            will be killed and assigned a game loss.
        """
        self.timeout = timeout

    def add_observer(self, observer):
        """Adds an observer, which will be sent the board, placements,
        turns, errors, and gameover in a timely manner.
        :param Observer observer: an Observer for this game
        """
        self.observer_manager.add_observer(observer)

    def _initialize(self):
        """Initialize game components and tell players what their id is
        :rtype PlayerResult.OK or tuple(PlayerResult.NEFARIOUS, Uuid):
            OK if initialization went fine.
            NEFARIOUS and the nefarious player otherwise.
        """
        self._reset_board()
        for player_uuid, player_guard in self.uuids_to_player.items():
            try:
                player_guard.set_id(player_uuid)
                name = player_guard.get_name()
                self.uuids_to_name[player_uuid] = name
            except PlayerError:
                return (PlayerResult.NEFARIOUS, player_uuid)
        return PlayerResult.OK

    def _play_game(self, players):
        """ Plays a game out and returns the result of the game.
        :param list players: List of two Uuids in order of who goes first
        :rtype tuple(PlayerResult, Uuid): the result of the game
        """
        # start phase
        for player in players:
            player_guard = self.uuids_to_player[player]
            try:
                player_guard.start_of_game()
            except PlayerError:
                return (PlayerResult.NEFARIOUS, player)
        # placement phase
        for worker_num in range(Worker.NUM_WORKERS):
            for player in players:
                current_player_guard = self.uuids_to_player[player]
                place_result = self._place_worker(current_player_guard)
                if place_result is PlayerResult.OK:
                    continue
                else:
                    return (place_result, player)
        # play phase
        id_and_players = zip(players, [self.uuids_to_player[player] for player in players])
        for player_uuid, player in itertools.cycle(id_and_players):
            turn_result = self._play_turn(player)
            if turn_result is PlayerResult.OK:
                continue
            else:
                return (turn_result, player_uuid)
            
            workers = [w for w in self.board.workers if w.player == player_uuid]
            if rulechecker.is_game_over(copy.deepcopy(self.board), workers):
                return (PlayerResult.OK, rulechecker.get_winner(self.board))

    def _place_worker(self, player):
        """Get a placement from a player and place on the board.
        :param PlayerGuard player: the PlayerGuard to get a placement from
        :rtype PlayerResult: OK if worker placement went through
                             BAD if worker placement was invalid
                             NEFARIOUS if player did something untrustworthy
        """
        try:
            worker, position = player.place_worker(copy.deepcopy(self.board))
        except PlayerInvalidPlacement:
            p_uuid = self._uuid_of_player_guard(player)
            self._notify_observers_player_bad_placement(p_uuid)
            return PlayerResult.BAD
        except PlayerError:
            p_uuid = self._uuid_of_player_guard(player)
            self._notify_observers_player_disqualified(p_uuid)
            return PlayerResult.NEFARIOUS
        else:
            self.board.place_worker(worker, position)
            self._notify_observers_placement((worker, position))
            return PlayerResult.OK

    def _play_turn(self, player):
        """Get a turn from a player and enact on the board.
        :param PlayerGuard player: the PlayerGuard to get a turn from
        :rtype PlayerResult: OK if turn went through
                             GIVE_UP if the player gave up
                             BAD if turn was invalid
                             NEFARIOUS if player did something untrustworthy
        """
        try:
            worker, move_dir, build_dir = player.play_turn(copy.deepcopy(self.board))
        except PlayerInvalidTurn:
            p_uuid = self._uuid_of_player_guard(player)
            self._notify_observers_player_bad_turn(p_uuid)
            return PlayerResult.BAD
        except PlayerError:
            p_uuid = self._uuid_of_player_guard(player)
            self._notify_observers_player_disqualified(p_uuid)
            return PlayerResult.NEFARIOUS
        else:
            if worker == None and move_dir == None and build_dir == None:
                p_uuid = self._uuid_of_player_guard(player)
                self._notify_observers_gave_up(self.uuids_to_name[p_uuid])
                return PlayerResult.GIVE_UP
            else:
                self._do_move(worker, move_dir, build_dir)
                self._notify_observers_turn((worker, move_dir, build_dir))
                return PlayerResult.OK

    def _do_move(self, worker, move_dir, build_dir=None):
        """Perform a turn on the board
        :param Worker worker: the worker that is moving
        :param Direction move_dir: the worker to move in
        :param Direction build_dir: the direction to build in
        """
        self.board.move_worker(worker, move_dir)
        if build_dir:
            self.board.build_floor(worker, build_dir)

    def _end_game(self, winner, evil_players):
        """ Notifies players of end of game.
        :param Uuid winner: uuid of winner
        :param list(Uuid) evil_players: the bad players
        """
        winner_name = self.uuids_to_name[winner]
        self._notify_observers_game_over(winner_name)
        # attempt to notify non bad players
        for player in self.uuids_to_player:
            if player not in evil_players:
                try:
                    self.uuids_to_player[player].end_of_game(winner_name)
                except PlayerError:
                    self._notify_observers_player_disqualified(player)
                    evil_players.append(player)
        # return all players that were bad, or just the winner
        if len(evil_players) is not 0:
            logging.error("bad players were" + str(evil_players))
            return (PlayerResult.NEFARIOUS, evil_players)
        else:
            logging.error("winner was" + str(winner))
            return (PlayerResult.OK, winner)

    def _determine_init_result(self, result):
        """ From a result, determine the winner and any misbehaving players.
        :param PlayerResult.OK or
               tuple(PlayerResult.NEFARIOUS, Uuid) result:
                   A result of initialization
        :rtype tuples(Uuid, list(Uuids)):
                The first element is NO_WINNER or the winning player's Uuid
                The second element list of bad players determined by the result
        """
        if result is PlayerResult.OK:
            return NO_WINNER, []
        elif result[0] is PlayerResult.NEFARIOUS:
            bad_players = result[1]
            player_ids = self.uuids_to_player.keys()
            winner = next(player_id for player_id in player_ids
                            if player_id is not bad_players)
            return  winner, [result[1]]

    def _determine_winner_result(self, result, evil_players=None):
        """ From a result, determine the winner and any misbehaving players.
        :param tuple(PlayerResult, Uuid) result: A result of a game phase
            (OK, Uuid) means that the Player won and the game was successful
            (GAVE_UP, Uuid) means that the Player ceded the game
            (BAD, Uuid) means that the Player was disqualified
            (NEFARIOUS, Uuid) means that the Player did something fishy
        :param list(Uuids) evil_players: players known to be fishy
        :rtype (Uuid, list(Uuid)):
            The first Player in the tuple is the uuid of the winner
        """
        if evil_players is None:
            evil_players = []

        if result is PlayerResult.OK:
            winner = player
        else:
            result, player = result
            winner = [p_id for p_id in self.uuids_to_player if p_id is not player][0]
            evil_players.append(player)

        return winner, evil_players

    def _uuid_of_player_guard(self, player_guard):
        """ Get the Uuid of a player_guard.
        :param PlayerGuard player_guard: the PlayerGuard to get the Uuid of
        :rtype Uuid or None: Returns the uuid if it is found, else None
        """
        for pg_uuid, pg in self.uuids_to_player.items():
            if pg == player_guard:
                return pg_uuid
        return None

    def _notify_observers_placement(self, placement):
        """Notify observers of placement.
        :param Placement placement: a placement of a worker
        """
        self.observer_manager.notify_all("update_placement", copy.deepcopy(self.board),
                                        copy.deepcopy(placement), self.uuids_to_name)

    def _notify_observers_turn(self, turn):
        """Notify observers of placement.
        :param Turn turn:
        """
        self.observer_manager.notify_all("update_turn", copy.deepcopy(self.board),
                                        turn, self.uuids_to_name)

    def _notify_observers_gave_up(self, player_name):
        """Notify observers of a player giving up.
        :param String player_name: the name of the player who gave up
        """
        self.observer_manager.notify_all("update_gave_up", player_name)

    def _notify_observers_game_over(self, winner):
        """Notify observers of game over
        :param Uuid winner: Uuid of winner
        """
        self.observer_manager.notify_all("update_game_over", copy.deepcopy(self.board),
                                        winner, self.uuids_to_name)

    def _notify_observers_error_msg(self, msg):
        """Notify observers of error message
        :param String msg: Error message
        """
        self.observer_manager.notify_all("update_error_msg", msg)

    def _notify_observers_player_disqualified(self, player):
        """ Notify observers that player is disqualified
        :param Uuid player: Uuid of disqualified player
        """
        player_name = self.uuids_to_name[player]
        error_msg = f"Player {player_name} is disqualified."
        self._notify_observers_error_msg(error_msg)
        
    def _notify_observers_player_bad_turn(self, player):
        """ Notify observers that player attempted a bad turn. 
        :param Uuid player: Uuid of infracting player
        """
        player_name = self.uuids_to_name[player]
        error_msg = f"Player {player_name} attempted a bad turn."
        self._notify_observers_error_msg(error_msg)

    def _notify_observers_player_bad_placement(self, player):
        """ Notify observers that player attempted a bad placement. 
        :param Uuid player: Uuid of infracting player
        """
        player_name = self.uuids_to_name[player]
        error_msg = f"Player {player_name} attempted a bad placement."
        self._notify_observers_error_msg(error_msg)

    def _reset_board(self):
        """ Resets the board """
        self.board = Board()
