import json
import sys

# TODO uncomment once actual code is received
# import server-for-given-2spread as server


class CircularityException(Exception):
    """Exception raised for circular spreadsheet references"""
    def __init__(self):
        self.message = "Circular formula"


def read_input():
    """Accepts input from STDIN and executes valid JSON spreadsheet commands"""
    # A dictionary mapping spreadsheet names to spreadsheet objects
    spreadsheets = {}
    # A mapping of opening characters to their closing character
    brackets = {'[': ']'}
    # The opening characters we have found that are not yet closed
    to_close = []
    # The current JSON we are adding to, until we have a complete JSON
    working_json = ''
    # Run continuously until STDIN is closed
    for line in sys.stdin:
        # Iterate through each character
        for c in line:
            if not to_close:
                if c in brackets:
                    working_json = c
                    to_close.append(c)
            else:  
                working_json += c
                # If we've closed a set of brackets
                if c == brackets[to_close[0]]:
                    to_close.pop()  # Keep track of how many are open
                    if not to_close:
                        # If we have reached the end of a JSON, execute it.
                        spreadsheets = execute(working_json, spreadsheets)
                        working_json = ''  # Reset working_json
                # If we've found another open bracket
                elif c == to_close[0]:
                    to_close.append(c)  # Keep track of how many are open


def execute(command_string, spreadsheets):
    """Execute a valid JSON value
    
    :param command_string: the input command as a string
    :param spreadsheets: the dictionary mapping of names to spreadsheets
    :return: the updated dictionary mapping of names to spreadsheets
    """
    command = json.loads(command_string)
    name = command[1]
    if command[0] == 'sheet':
        s = server.Spreadsheet()  # TODO this will work with anticipated Codemanistan code
        spreadsheets.update({name:s.build_spreadsheet(command[2])})
    if command[0] == 'set':
        spreadsheets[name].set_value(command[2], command[3], command[4])
    if command[0] == 'at':
        try:
            print(spreadsheets[name].get_value(command[2], command[3]))
        except CircularityException:
            print('false')
    return spreadsheets