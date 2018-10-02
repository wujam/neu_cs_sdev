# 6
## Files
- aux: folder for auxillary files
  - parse_json.py: library file to parse json objects from a string
  - board.py: implementation of the Santorini Board
- xboard: systems level test harness for the board implementation
- board-tests: contains sample input and outputs to use with xboard
  - X-in.json (X between 1 and 5 inclusive)
  - X-out.json (X between 1 and 5 inclusive)

The tests can be run by redirecting the X-in.json into xboard and using diff
with the output of xboard and the corresponding X-out.json

ex:
`./xboard < X-in.json | diff - X-out.json`

it should print nothing if the test is successful
