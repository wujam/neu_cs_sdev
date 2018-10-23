#!/usr/bin/python3.6
"""Implementation of the referee in Santorini."""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.pieces import Board
from Santorini.Common import rulechecker
import itertools
import copy

class Referee():
    """Implementation of the Referee component in Santorini."""

    NUM_WORKERS = 2

    def __init__(self, players):
        """Create a referee component with the associated list of players."""
        self.players = players
        self.board = Board()
        self.turn = 0

    def run_game(self):
        """Supervise a game between players.

        A referee will be able to construct a new board and have
        access to the rules. The ref will then initialize each player
        and then determine the "first" player in the game.

        The ref will receive the player's worker placements and then
        place them, in alternating order, on the board.

        During the course of the game, the ref will call complete_turn
        to execute turns given to him by the player.

        If a game end state is reached, the ref will call determine_winner
        to check against its list of players and the board to get the
        winner of the game. 
        rtype: the player that one the game
        """

        # reset the game so previous state from another game
        # won't affect this game
        self._reset()

        game_players = copy.copy(self.players)

        # call player initialize methods at the start
        for player in game_players:
            player.initialize()

        # place the player workers on the board
        for worker in range(self.NUM_WORKERS):
            for player in game_players:
                # player made a bad placement
                if not self.complete_placement(player):
                    # if the game shouldn't continue finish it
                    if not self._lose_player(player, game_players):
                        game_players[0].game_over(True)
                        return game_players[0]

        # turn loop over all the players
        for player in itertools.cycle(game_players):
            # if the given turn was not valid
            if not self.complete_turn(player):
                # if the game shouldn't continue finish it
                if not self._lose_player(player, game_players):
                    game_players[0].game_over(True)
                    return game_players[0]

            # check if the game is over
            if rulecheker.is_game_over(self.board, player.workers):
                player.game_over(True)
                losers = [winner for winner in game_players if winner is not player]
                for loser in losers:
                    loser.game_over(False)
                    return player

    def run_n_games(self, num_games):
        """Supervises a best of num_games game series with the two players

        Will call run_game num_games times and tally up the score

        param: num_games the number of games to play in this series
                         this should be an odd number
        rtype: the player that won the game series
        """

        player_scores = [0] * len(self.players)

        # a dict mapping players to the number of games they won
        for i in range(num_games):
            player_won = run_game()
            players_scores[self.players.index(player)] += 1

        won_player = None
        won_player_score = 0

        for i in range(len(player_scores)):
            if player_scores[i] > won_player_score:
                won_player_score = player_scores[i]
                won_player = self.players[i]

        return won_player

    def _lose_player(self, player, game_players):
        """Kick a player out of the game

        Tell the player that they lost

        Check if there is more than 1 player
        left in the game or not
        rtype: bool
                True if the game should continue (more than 1 player)
                False if the game is over (only 1 player left)
        """

        player.game_over(True)

        # remove player from the player list
        game_players = [winner for winner in game_players if winner is not player]

        return True if len(self.players) == 1 else False

    def complete_placement(self, player):
        """Complete a placement for a given player.

        This method will call the player's place_worker method in
        conjunction with the rulecheker.

        If the turn is invalid, the ref will end the game and
        declare the opposing player as the winner.

        :param player: the player who is placing a worker
        :rtype bool
                True if the placement was valid
                False if there was a problem
        """

        worker, pos = player.place_worker(self.board)
        # check if the turn isn't valid
        if not rulechecker.can_place_worker(copy.deepcopy(self.board), worker, pos):
            return False

        self.board.place_worker(worker, pos)
        return True

    def complete_turn(self, player):
        """Complete a turn for a given player.

        This method will call the player's play_turn method in
        conjunction with the rulechecker.

        If the turn is invalid, the ref will end the game and
        declare the opposing player as the winner.

        A turn is one of:
        (None, None, None) - A no request if it couldn't find any move
        (Worker, Direction, None) - Move request
        (Worker, Direction, Direction). - Move+Build request

        :param player: the player who's turn it is
        :rtype bool
                True if the turn is valid
                False if there was a problem
        """

        # TODO process isolation for players
        # don't need to deepcopy the board
        # because it will be running in a fork
        # TODO can we run just the method in a separate process
        # what if the player wants to keep state around between turns?

        # get the next turn the player wants to make
        worker, move_dir, build_dir = player.play_turn(copy.deepcopy(self.board))

        # check case where no move is returned
        if worker is None:
            return False
        
        # check if the turn isn't valid
        # TODO make rulechecker can_move_build return False
        #   if the given move is not a winning move
        #   or if a given move + build moves onto a
        #   3 height spot
        if not rulechecker.can_move_build(self.board, move_dir, build_dir):
            return False

        # apply move to the board since it's valid
        self.board.move_worker(worker, move_dir)

        # apply build_dir to the board if there is one
        if build_dir is not None:
            self.board.build_floor(worker, build_direction)

        return True

    def _reset(self):
        """resets the state of the referee.

        Resets the game board"""
        self.board = Board()
