"""A wrapper around jsonschema to check if a given JSON is valid or not
"""
#import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), "../jsonschema"))
from jsonschema import validate, ValidationError

def validate_json(schema, data):
    """
    Validates the data with the given jsonschemas path
    :param Json schema: Name of the json schema to validate with
    :param Json data: Json object to validate
    :rtype bool: True if data matches the schema, False otherwise
    """
    try:
        validate(data, schema)
    except ValidationError:
        return False
    return True
