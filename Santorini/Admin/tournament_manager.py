import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import json
import uuid
import collections
import itertools
import inspect
import importlib
import importlib.util
from Santorini.Admin.referee import Referee
from Santorini.Admin.observermanager import ObserverManager
from Santorini.Common.player_guard import *
from Santorini.Common.observer_interface import AbstractObserver
from Santorini.Common.player_interface import AbstractPlayer
from Santorini.Lib.json_validate import validate_json
from Santorini.Lib.dyn_import import find_subclass_in_source
from Santorini.Common.jsonschemas import PLAYER, OBSERVER
from Santorini.Admin.jsonschemas import ADMIN_CONFIG
"""A Tournament Manager for Santorini meet_ups"""

class TournamentManager:

    MEET_UP_GAMES = 3

    def __init__(self, timeout=60):
        self.uuids_players = collections.OrderedDict()
        self.uuids_names = collections.OrderedDict()
        self.observer_manager = ObserverManager()
        self.nef_players = []
        self.meet_up_results = []
        self.timeout = timeout

    def read_config_from(self, file_in=sys.stdin):
        """Reads the tournament configuration from an input IO object
        :param IO file_in: the IO object to read the config from
        """
        in_str = file_in.read()
        in_json = json.loads(in_str)

        if not validate_json(ADMIN_CONFIG, in_json):
            raise ValueError("Bad Config, did not validate")

        for player_spec in in_json["players"]:
            if validate_json(PLAYER, player_spec):
                self._add_player(player_spec)

        for observer_spec in in_json["observers"]:
            if validate_json(OBSERVER, observer_spec):
                self._add_observer(observer_spec)

    def run_tournament(self):
        """Runs a round robin tournament with the configured players

        A meet_up result is a 2 element list with the first element being the
        name of the winner and the second being the name of the loser

        :rtype (List of names of misbehaving players,
               list of meet_up results in the order played):
        """
        matches = itertools.combinations(self.uuids_players.keys(),
                                         Referee.NUM_PLAYERS)

        filtered_matches = itertools.filterfalse(
            lambda match: any(player in self.nef_players for player in match),
            matches)

        for match in filtered_matches:
            match_uuids_players = {match[0] : self.uuids_players[match[0]],
                                   match[1] : self.uuids_players[match[1]]}
            match_uuids_names = {match[0] : self.uuids_names[match[0]],
                                 match[1] : self.uuids_names[match[1]]}

            self.uuids_players[match[0]].set_opponent(
                match[1],self.uuids_names[match[1]])
            self.uuids_players[match[1]].set_opponent(
                match[0], self.uuids_names[match[0]])

            ref = Referee(match_uuids_players, match_uuids_names,
                          self.observer_manager)
            nef_players, game_winners = ref.run_n_games(self.MEET_UP_GAMES)

            self.nef_players.extend(nef_players)

            if len(nef_players) == 1:
                self._filter_bad_meet_up_results()
                meet_up_winner = [player for player in match if player != nef_players[0]][0]
            elif len(nef_players) == 2:
                self._filter_bad_meet_up_results()
                continue
            else:
                meet_up_winner = max(match, key=game_winners.count)

            meet_up_result = self._winner_to_meet_up_result(match, meet_up_winner)
            self.meet_up_results.append(meet_up_result)

        return [self.uuids_names[uuid] for uuid in self.nef_players], \
               [[self.uuids_names[uuid] for uuid in meet_up_result]
                for meet_up_result in self.meet_up_results]

    def _filter_bad_meet_up_results(self):
        """removes invalid meet_ups (meet_ups in which both players broke),
           reverses the winner and loser of meet_ups where bad players previously won
        """
        invalid_meet_ups = []
        for meet_up_result in self.meet_up_results:
            if meet_up_result[0] in self.nef_players:
                if meet_up_result[1] in self.nef_players:
                    invalid_meet_ups.append(meet_up_result)
                else:
                    meet_up_result.reverse()

        for meet_up_result in invalid_meet_ups:
            self.meet_up_results.remove(meet_up_result)

    def _winner_to_meet_up_result(self, player_ids, winner):
        """Generates a meet_up result based on the given players and
           the given winner
        :param list of 2 UUIDs player_ids: list of 2 player UUIDs
        :param UUID winner: the uuid of the winner
        """
        if winner == player_ids[0]:
            return player_ids
        else:
            return player_ids[::-1]

    def _add_observer(self, observer_spec):
        """Adds an observer to the tournament
        :param [str, str] observer: the spec for an observer which is
                                    the name, and path to the observer
        """
        _, path = observer_spec

        observer_class = find_subclass_in_source(path, AbstractObserver)

        if observer_class:
            self.observer_manager.add_observer(observer_class())

    def _add_player(self, player_spec):
        """Adds a player to the tournament from a spec
        :param [str, str, str] player: the spec for a player which is
                                       the kind, name, and path to the player
        """
        _, name, path = player_spec
        if not self._validate_name(name):
            return
        uniq_name = self._gen_unique_name(name)
        new_name = True if uniq_name != name else False

        player_class = find_subclass_in_source(path, AbstractPlayer)
        if player_class:
            player_guard = PlayerGuard(player_class(), timeout=self.timeout)
            player_uuid = uuid.uuid4()
            try:
                player_guard.set_id(player_uuid)
                player_guard.set_name(uniq_name, new_name=new_name)
            except PlayerError:
                return
            self.uuids_players[player_uuid] = player_guard
            self.uuids_names[player_uuid] = uniq_name

    def _add_player_direct(self, player, name):
        """Adds a player object directly to the tournament
        :param Player player: the player to be added
        """
        if not self._validate_name(name):
            return
        uniq_name = self._gen_unique_name(name)
        new_name = True if uniq_name != name else False

        player_guard = PlayerGuard(player, timeout=self.timeout)
        player_uuid = uuid.uuid4()
        try:
            player_guard.set_id(player_uuid)
            player_guard.set_name(uniq_name, new_name=new_name)
        except PlayerError:
            return
        self.uuids_players[player_uuid] = player_guard
        self.uuids_names[player_uuid] = uniq_name

    def _validate_name(self, name):
        """validates that the string is lowercase and only has letter
        :param str name: the name to be validated
        :rtype bool: True if name is valid, False otherwise
        """
        return name.isalpha() and name.islower()

    def _gen_unique_name(self, name):
        """If the given name is unique from the current list of names return it,
           Otherwise return a unique name
        :param str name: the given name
        :rtype str
        """

        cur_names = self.uuids_names.values()

        new_name = name
        suffix = "a"
        while new_name in cur_names:
            new_name = name + str(suffix)
            suffix += "a"

        return new_name
