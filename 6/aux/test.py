#!/usr/bin/env python3
import os
import json
import jsonschema
from jsonschema import validate

instance = ['']

schema = {'type': 'array', 'items': {'$ref': 'address.json'}}

resolver = jsonschema.RefResolver("file://%s/jsonschemas/" % os.path.abspath(os.path.dirname(__file__)), schema)

print("file://%s/jsonschemas/" % os.path.abspath(os.path.dirname(__file__)))

print(validate(instance, schema, resolver=resolver))
