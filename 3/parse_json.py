import sys
import json

def parse_json(in_str):
    """
    Takes a json in String form and parses it.
    in_str: String, input json with multiple lines
    return: String, the json values in reverse position on separate lines embedded
                    in a json array indicating the reverse position.
                    e.g.
                    input:
                    [1,2]
                    {"a":1}
                    output:
                    [1,[1,2]]
                    [0,{"a":1}]
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

    for i in range(len(in_exprs)):
        print(json.dumps([len(in_exprs) - i - 1, in_exprs[i]], separators=(",", ":")))
