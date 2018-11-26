"""JSON schemas that Admin components use for validation"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from Santorini.Common.jsonschemas import PLAYER, OBSERVER

ADMIN_CONFIG = {
    "type": "object",
    "properties": {
        "players": {
            "type": "array",
            "items": PLAYER
        },
        "observers": {
            "type": "array",
            "items": OBSERVER
        }
    },
    "required": ["players", "observers"],
    "additionalProperties": False
}
