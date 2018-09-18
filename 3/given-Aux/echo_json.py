import sys


def read_input():
    """Accumulates input from STDIN until EOF"""
    # Initialize string of user input
    lines = ""

    # Run continuously until STDIN is closed
    for line in sys.stdin:
        # Add user inputs to accumulating string
        lines += line
    
    return lines


def process(lines):
    """
    Return all the given JSON values, each on a separated line, embedded in a JSON array
    that indicates its reverse position in the stream (counting down to 0)
    :param lines: a string of potential JSON values
    """
    # Initialize list of JSONs
    jsons = []
    values = ['true', 'false', 'null']
    # A mapping of opening characters to their closing character
    brackets = {'[': ']', '{': '}', '"': '"'}
    # The opening characters we have found that are not yet closed
    to_close = []
    # The current JSON we are adding to, until we have a complete JSON
    working_json = ''

    # Iterate through each character
    for c in [l for l in lines if l != '\n']:
        if not to_close:
            if working_json.isnumeric() and not c.isnumeric():
                jsons.append(working_json)
                working_json = ''
            if c in brackets:
                working_json = c
                to_close.append(c)
            else:
                working_json += c
                for v in values:
                    if v in working_json:
                        jsons.append(v)
                        working_json = ''
        else:  
            working_json += c
            if c == brackets[to_close[0]]:
                to_close.pop()
                if not to_close:
                    jsons.append(working_json)
                    working_json = ''
            elif c == to_close[0]:
                to_close.append(c)

    output = ''
    # Calculate the number of JSONS for displaying the reverse position
    rev_pos = len(jsons)
    # Store all the JSON values, each on a separated line, embedded in a JSON array
    # that indicates its reverse position in the stream (counting down to 0).
    for i in range(0, len(jsons)):
        rev_pos -= 1
        output += '[{0},{1}]'.format(rev_pos, jsons[i]) + '\n'

    return output
