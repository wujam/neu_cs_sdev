"""JSON schemas that Common components use for validation"""

PLAYER = {
    "type": "array",
    "items": [
        {
            "type": "string",
            "enum": ["good", "breaker", "infinite"]
        },
        {
            "type": "string"
        },
        {
            "type": "string"
        }
    ],
    "minItems": 3,
    "additionalItems": False
}

OBSERVER = {
    "type": "array",
    "items": [
        {
            "type": "string"
        },
        {
            "type": "string"
        }
    ],
    "minItems": 2,
    "additionalItems": False
}

