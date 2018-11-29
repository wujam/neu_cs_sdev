import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import itertools
import unittest
from Santorini.Common import pieces
from Santorini.Lib.json_validate import validate_json
from Santorini.Remote import jsonschemas

# common JSON artifacts to test
# all tuples of direction, e.g. ("EAST", "NORTH"), ("EAST", "PUT"), ...
all_dir_tuples = pieces.DIR_TABLE.keys()

# valid Names
# a valid Name is a string of lowercase characters
names = ["a", "asdfhasouasdfaqwertyuiopasdfghjklzxcvbnm", "bjapojapjpoajjijrq", "z"]
# "" is not considered a valid Name
# an invalid Name contains non-alphabetic characters and non-lowercase characters
invalid_names = ["AASDFASDFADF", "asafFsdsf", "1x02u9,0@$@>!/.,c34c92ASFD084\\\n\n\r", ""]

# valid Workers
# a valid Worker is a valid Name followed by 1 or 2
workers = [name + str(num) for num, name in itertools.product([1,2], names)] 
# a Worker with an invalid Name is invalid 
invalid_workers = [name + str(num) for num, name in itertools.product([1,2], invalid_names)] 
# Workers cannot start with numbers
invalid_workers += [str(num) + name for num, name in itertools.product([1,2], names + invalid_names)] 

# valid Actions are one of
# String or
# (Worker, EastWest, NorthSouth) or
# (Worker, EastWest, NorthSouth, EastWest, NorthSouth)
actions = [[worker] + list(dir_tuple) for worker, dir_tuple in itertools.product(workers, all_dir_tuples)]
actions += [[worker] + list(dir_tuple) + list(dir_tuple2) for worker, dir_tuple, dir_tuple2 in itertools.product(workers, all_dir_tuples, all_dir_tuples)]
# invalid actions contain invalid workers or invalid directions
invalid_actions = [(worker,) + dir_tuple for worker, dir_tuple in itertools.product(invalid_workers, all_dir_tuples)]
invalid_actions += [(worker,) + dir_tuple + dir_tuple2 for worker, dir_tuple, dir_tuple2 in itertools.product(invalid_workers, all_dir_tuples, all_dir_tuples)]
invalid_actions += [(worker,) for worker in invalid_workers]
# (NorthSouth, EastWest) instead of (EastWest, NorthSouth)
invalid_actions += [(worker,) + (dir_tuple[1], dir_tuple[0]) for worker, dir_tuple in itertools.product(workers, all_dir_tuples)] 

# valid Coordinates are natural numbers in [0,5]
coordinates = [num for num in range(6)]
# invalid Coordinates are non-numbers, non-integers, or integers less than 0 or greater than 5
invalid_coordinates = ["potato", 1.29495, -2.2323, -5, 192]

# valid WorkerPlaces are (Worker, Coordinate, Coordinate)
worker_places = list(itertools.product(workers, coordinates, coordinates))
# invalid WorkerPlaces are not that
invalid_worker_places = [["blah", "blah", "blah"], ["worker1"], "(\"worker1\", 2, 2)", []]
invalid_worker_places += list(itertools.product(invalid_workers, invalid_coordinates, invalid_coordinates))

# valid Places are (Coordinate, Coordinate)
places = [p for p in itertools.product(coordinates, coordinates)]
# invalid Places are not that
invalid_places = list(itertools.product(invalid_coordinates, invalid_coordinates))

# valid Placements are [WorkerPlace, ...] of up to 3 WorkerPlaces
placements = [[]]
placements += [[wp] for wp in worker_places]
placements += list(itertools.product(worker_places, worker_places))
placements += list(itertools.product(worker_places, worker_places, worker_places))
# invalid Placements are not that
invalid_placements = ["potato", [["potato", 2, 2], ["potato", 1, 1]], ["potato", "potato", "potato"]]
invalid_placements += [[["potato", 2, 2], ["potato", 2, 2], ["potato", 2, 2], ["potato", 2, 2]]] 
invalid_placements += [["potato", ["potato", 2, 2]]] 
invalid_placements += [[wp] for wp in invalid_worker_places]

# valid EncounterOutcomes are (String, String) or (String, String, "irregular")
encounter_outcomes = [["potato", "tomato"], ["potato", "tomato", "irregular"]]
# invalid EncounterOutcomes are not that
invalid_encounter_outcomes = [["potato"], ["potato", "tomato", "somewhat-irregular"], ["potato", "tomato", "irregular", "blah"]]

# valid Results are arrrays of EncounterOutcomes
resultss = [[]] + [[outcome] for outcome in encounter_outcomes]
resultss += list(itertools.product(encounter_outcomes, encounter_outcomes))
resultss += [["potato", "tomato"], ["potato", "tomato"], ["potato", "tomato", "irregular"]]

action_tests = \
    [("player", True),
    ("PlaYer", False),
    ("--_aslk2345678=<=s>dtfs789_-@#%@!%%#%#@,./,.3,/4,2/.3,4\\\"])[(^&*`~?/\n\t\r", False),
    (1, False),
    (0, False),
    (2, False),
    (jsonschemas, False)]
action_tests += [(action, True) for action in actions]
action_tests += [(action, False) for action in invalid_actions]

board_tests = []
board_row_tests = []
building_worker_tests = []
cell_tests = []
client_config_tests = []
coordinate_tests = [(coord, True) for coord in coordinates] 
coordinate_tests += [(coord, False) for coord in invalid_coordinates] 
encounter_outcome_tests = [(outcome, True) for outcome in encounter_outcomes] 
encounter_outcome_tests += [(outcome, False) for outcome in invalid_encounter_outcomes] 
height_tests = [(height, True) for height in range(4)]
name_tests = [(name, True) for name in names]
name_tests += [(name, False) for name in invalid_names]
observer_tests = []
place_tests = [(place, True) for place in places] 
place_tests += [(place, True) for place in invalid_places] 
placement_tests = [(placement, True) for placement in placements] 
placement_tests += [(placement, False) for placement in invalid_placements] 
player_tests = [] 
playing_as_tests = [(pl, True) for pl in list(itertools.product(["playing-as"], names))]
playing_as_tests += [(pl, False) for pl in list(itertools.product(["playing-as"], invalid_names))]
playing_as_str_tests = [("playing-as", True), ("potato", False)] 
results_tests = [(results, True) for results in resultss]
server_config_tests = []
worker_tests = [(worker, True) for worker in workers] 
worker_tests += [(worker, False) for worker in invalid_workers] 
worker_place_tests = [(wp, True) for wp in worker_places] 
worker_place_tests = [(wp, False) for wp in invalid_worker_places] 
_direction_items_tests = []

json_schema_tests = [
    ["ACTION", action_tests],
    ["BOARD", board_tests],
    ["BOARD_ROW", board_row_tests],
    ["BUILDING_WORKER", building_worker_tests],
    ["CELL", cell_tests],
    ["CLIENT_CONFIG", client_config_tests],
    ["COORDINATE", coordinate_tests],
    ["ENCOUNTER_OUTCOME", encounter_outcome_tests],
    ["HEIGHT", height_tests],
    ["NAME", name_tests],
    ["OBSERVER", observer_tests],
    ["PLACE", place_tests],
    ["PLACEMENT", placement_tests],
    ["PLAYER", player_tests],
    ["PLAYING_AS", playing_as_tests],
    ["PLAYING_AS_STR", playing_as_str_tests],
    ["RESULTS", results_tests],
    ["SERVER_CONFIG", server_config_tests],
    ["WORKER", worker_tests],
    ["WORKER_PLACE", worker_place_tests],
    ["_DIRECTION_ITEMS", _direction_items_tests],
]

class TestRemoteJsonschemas(unittest.TestCase):
    """ Test the remote json schemas """
    TEST_MSG = "Testing test_{schema_name}_{num}"

    def test_json_validation(self):
        for schema_name, schema_tests in json_schema_tests:
            schema = TestRemoteJsonschemas.get_schema(schema_name)

            for test_num, (schema_test, expected_result) in enumerate(schema_tests): 
                test_msg = TestRemoteJsonschemas.TEST_MSG.format(schema_name=schema_name, num=test_num)
                self.run_validation_subtest(test_msg, schema, schema_test, expected_result)

    @staticmethod
    def get_schema(name):
        """
        Gets the named schema from jsonschemas
        :param String name: name of the schema in jsonschemas
        :rtype JsonSchema or None: the jsonschema found
        """
        return getattr(jsonschemas, name, None)

    def run_validation_subtest(self, msg, schema, schema_test, expected):
        """
        Runs a json validation test using the given schema on the given test string
        :param String msg: a test message
        :param JsonSchema schema: the schema to validate against
        :param JsonString schema_test: the Json String to be validated
        :param bool expected: the expected result
        """
        with self.subTest(msg, schema_test=schema_test,expected_result=expected):
            self.assertEqual(validate_json(schema, schema_test), expected)


