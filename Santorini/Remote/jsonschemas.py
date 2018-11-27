"""JSON schemas that Remote components use for validation"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.jsonschemas import PLAYER, OBSERVER

SERVER_CONFIG = {
    "type": "object",
    "properties": {
        "min_players": {
            "type": "integer",
            "minimum": 1
        },
        "port": {
            "type": "integer",
            "minimum": 1
        },
        "waiting for": {
            "type": "integer",
            "minimum": 1
        },
        "repeat": {
            "type": "integer",
            "minimum": 0,
            "maximum": 1
        }
    },
    "required": ["min_players", "port", "waiting for", "repeat"],
    "additionalProperties": False
}

CLIENT_CONFIG = {
    "type": "object",
    "properties": {
        "players": {
            "type": "array",
            "items": PLAYER
        },
        "observers": {
            "type": "array",
            "items": OBSERVER
        },
        "ip": {
            "type": "string"
        },
        "port": {
            "type": "integer",
            "minimum": 50000,
            "maximum": 60000
        }
    },
    "required": ["players", "observers", "ip", "port"],
    "additionalProperties": False
}

NAME = {
    "type": "string",
    "pattern": "^[a-z]*$"
}

PLAYING_AS_STR = "playing-as"

PLAYING_AS = {
    "type": "array",
    "items": [
        {
            "type": "string",
            "enum": [PLAYING_AS_STR]
        },
        NAME
    ],
    "minItems": 2,
    "additionalItems": False
}

COORDINATE = {
    "type": "integer",
    "minimum": 0,
    "maximum": 5
}

PLACE = {
    "type": "array",
    "items": [
        COORDINATE,
        COORDINATE
    ],
    "minItems": 2,
    "additionalItems": False
}

WORKER = {
    "type": "string",
    "pattern": "^[a-z]*[12]$"
}

WORKER_PLACE = {
    "type": "array",
    "items": [
        WORKER,
        COORDINATE,
        COORDINATE
    ],
    "minItems": 3,
    "additionalItems": False
}

PLACEMENT = {
    "type": "array",
    "items": WORKER_PLACE,
    "maxItems": 3
}

HEIGHT = {
    "type": "integer",
    "minimum": 0,
    "maximum": 4
}

BUILDING_WORKER = {
    "type": "string",
    "pattern": "^[0-4][a-z]*[12]$"
}

CELL = {
    "oneOf": [
        HEIGHT,
        BUILDING_WORKER
    ]
}

BOARD_ROW = {
    "type": "array",
    "items": CELL,
    "maxItems": 6
}

# manual check for four workers needs to be done
BOARD = {
    "type": "array",
    "items": BOARD_ROW,
    "maxItems": 6
}

_DIRECTION_ITEMS = [
    {
        "type": "string",
        "enum": ["EAST", "PUT", "WEST"]
    },
    {
        "type": "string",
        "enum": ["NORTH", "PUT", "SOUTH"]
    }
]

ACTION = {
    "oneOf": [
        NAME,
        {
            "type": "array",
            "items": [
                WORKER
            ] + _DIRECTION_ITEMS,
            "minItems": 3,
            "additionalItems": False
        },
        {
            "type": "array",
            "items": [
                WORKER
            ] + _DIRECTION_ITEMS + _DIRECTION_ITEMS,
            "minItems": 5,
            "additionalItems": False
        }
    ]
}

ENCOUNTER_OUTCOME = {
    "oneOf": [
        {
            "type": "array",
            "items": [
                NAME,
                NAME
            ],
            "minItems": 2,
            "additionalItems": False
        },
        {
            "type": "array",
            "items": [
                NAME,
                NAME,
                {
                    "type": "string",
                    "enum": ["irregular"]
                }
            ],
            "minItems": 3,
            "additionalItems": False
        }
    ]
}

RESULTS = {
    "type": "array",
    "items": ENCOUNTER_OUTCOME
}
