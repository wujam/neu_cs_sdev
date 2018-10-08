#!/usr/bin/env python
import sys
import json

def parse_json(in_str):
    """
    Takes a json in String form and parses it.
    in_str: String, input json with multiple lines
    return: List of JSON expressions
    """
    in_exprs = []
    out_exprs = []

    # JSON decoder to decode JSON objects
    decoder = json.JSONDecoder()

    # strips whitespace from the input string because it can
    # mess up the JSON decoder
    in_str.lstrip()

    # loop to get separate and store JSON objects
    while in_str:
        expr, index = decoder.raw_decode(in_str)
        in_exprs.append(expr)
        in_str = in_str[index:].lstrip()

    return in_exprs


