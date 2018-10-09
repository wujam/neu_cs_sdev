# 7
## Files
- aux: folder for auxillary files
  - parse_json.py: library file to parse json objects from a string
- xrules: systems level test harness for the rules implementation
- board-tests: contains sample input and outputs to use with xboard
  - X-in.json (X between 1 and 5 inclusive)
  - X-out.json (X between 1 and 5 inclusive)

The tests can be run by redirecting the X-in.json into xboard and using diff
with the output of xboard and the corresponding X-out.json

ex:
`./xrules < X-in.json | diff - X-out.json`

it should print nothing if the test is successful

There is also a TESTME script that can be run and it will print out the number of tests that passed/failed
