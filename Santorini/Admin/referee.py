#!/usr/bin/python3.6
"""Implementation of the referee in Santorini."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import Board, Worker
from Santorini.Common import rulechecker
from Santorini.Admin.player_guard import *
import itertools
import copy
import uuid
from enum import Enum
import logging
logging.basicConfig(filename='refereetest.log', filemode='w')

class PlayerResult(Enum):
    OK = 0
    BAD = 1
    NEFARIOUS = 2
class Referee:

    """Implementation of the Referee component in Santorini."""
    NUM_PLAYERS = 2

    def __init__(self, uuids_players, timeout=30):
        """Create a referee component with the associated list of players."""
        self.players = []
        self.timeout = timeout
        self.uuids_to_player = {}
        self.uuids_to_name = {}
        for uuid, player in uuids_players:
            player_guard = PlayerGuard(player, timeout=self.timeout)
            self.uuids_to_player[uuid] = player_guard
            self.players.append(player_guard)

    def run_game(self):
        """Supervise a game between players.
        :rtype tuple(PlayerResult.OK, Uuid) the player won the game
               tuple(PlayerResult.NEFARIOUS, list(Uuid)) the player did something
                                                         untrustworthy and the
                                                         other should win by
                                                         default
        """
        result = self._initialize()
        evil_players = []
        winner = None 
        if result is not PlayerResult.OK:
            evil_players.append(result[1])
            winner = [p for p in self.uuids_to_player if p != result[1]][0]
        else:
            result, player = self._play_game(self.uuids_to_player.keys())

            if result is PlayerResult.OK:
                winner = player
            else:
                winner = [p_id for p_id in self.uuids_to_player if p_id is not player][0]
            if result is PlayerResult.NEFARIOUS:
                evil_players.append(player)

        return self._end_game(winner, evil_players)

    def run_n_games(self, num_games):
        """Supervises a best of num_games game series with the two players

        Will call run_game num_games times and tally up the score

        :param int num_games: the number of games to play in this series
                              this should be an odd number
        :rtype tuple(PlayerResult.OK, Uuid) the player won the series
               tuple(PlayerResult.NEFARIOUS, list(Uuid)) the player did something
                                                         untrustworthy and the
                                                         other should win by
                                                         default
        """

        player_scores = [0] * len(self.players)
        result = self._initialize()
        evil_players = []
        player_ids = [p_id for p_id in self.uuids_to_player]
        logging.error("run n games")

        if result is not PlayerResult.OK:
            evil_players.append(result[1])
        else:
            # a dict mapping players to the number of games they won
            for i in range(num_games):
                logging.error("game" + str(i))
                self._reset_board()
                player_order = player_ids if i % 2 == 0 else [i for i in reversed(player_ids)]
                result, player = self._play_game(player_order)
                if result is PlayerResult.OK:
                    winner = player
                else:
                    winner = [p_id for p_id in self.uuids_to_player if p_id is not player][0]
                if result is PlayerResult.NEFARIOUS:
                    evil_players.append(player)

                endresult, players = self._end_game(winner, copy.deepcopy(evil_players))
                if endresult is PlayerResult.NEFARIOUS:
                    for p in players:
                        evil_players.append(p)
                if result is PlayerResult.NEFARIOUS or endresult is PlayerResult.NEFARIOUS:
                    break
                player_scores[player_ids.index(winner)] += 1

        logging.error("endloop")
        if len(evil_players) > 0:
            return (PlayerResult.NEFARIOUS, evil_players)
        else:
            won_player = None
            won_player_score = 0

            for i in range(len(player_scores)):
                if player_scores[i] > won_player_score:
                    won_player_score = player_score[i]
                    won_player = player_ids[i]

            return (PlayerResult.OK, won_player)

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
        """
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
            logging.error("placing")
            for player in players:
                player_guard = self.uuids_to_player[player]
                place_result = self._place_worker(player_guard)
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
            logging.error("placing" + str(worker) + str(position))
        except PlayerError:
            return PlayerResult.NEFARIOUS

        if rulechecker.can_place_worker(self.board, worker, position):
            self.board.place_worker(worker, position)
            return PlayerResult.OK
        else:
            return PlayerResult.BAD

    def _play_turn(self, player):
        """Get a turn from a player and enact on the board.
        :param PlayerGuard player: the PlayerGuard to get a turn from
        :rtype PlayerResult: OK if turn went through
                             BAD if turn was invalid
                             NEFARIOUS if player did something untrustworthy
        """
        try:
            worker, move_dir, build_dir = player.play_turn(copy.deepcopy(self.board))
        except PlayerError:
            return PlayerResult.NEFARIOUS

        can_move_build = rulechecker.can_move_build(copy.deepcopy(self.board), worker, move_dir, build_dir)
        is_winner = rulechecker.get_winner(copy.deepcopy(self.board))
        if can_move_build or is_winner:
            self._do_move(worker, move_dir, build_dir)
            return PlayerResult.OK
        else:
            return PlayerResult.BAD

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
        logging.error(str(len(evil_players)))
        winner_name = self.uuids_to_name[winner]
        for player in self.uuids_to_player:
            if player not in evil_players:
                try:
                    self.uuids_to_player[player].end_of_game(winner_name)
                except PlayerError:
                    evil_players.append(player)
        if len(evil_players) is not 0:
            return (PlayerResult.NEFARIOUS, evil_players)
        else:
            return (PlayerResult.OK, winner)

    def _reset_board(self):
        """ Resets the board """
        self.board = Board()
