import jsonschema
from jsonschema import validate

def validate_json(schema, data):
    """
    Validates the data with the given jsonschemas path
    :param str schema: Name of the json schema to validate with
    :param Json data: Json object to validate
    :rtype bool: True if data matches the schema, False otherwise
    """
