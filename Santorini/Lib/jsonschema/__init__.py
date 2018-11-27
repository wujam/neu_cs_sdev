"""
An implementation of JSON Schema for Python

The main functionality is provided by the validator classes for each of the
supported JSON Schema versions.

Most commonly, :func:`validate` is the quickest way to simply validate a given
instance under a schema, and will create a validator for you.

"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from Santorini.Lib.jsonschema.exceptions import (
    ErrorTree, FormatError, RefResolutionError, SchemaError, ValidationError
)
from Santorini.Lib.jsonschema._format import (
    FormatChecker, draft3_format_checker, draft4_format_checker,
)
from Santorini.Lib.jsonschema.validators import (
    Draft3Validator, Draft4Validator, RefResolver, validate
)

from Santorini.Lib.jsonschema._version import __version__

# flake8: noqa
