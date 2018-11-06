# 11
## Files
- xrun: systems level test harness for Santorini
- santorini.rc: contains sample input and outputs to use with xrun
  - X-in.json (X between 1 and 1 inclusive)
  - X-out.json (X between 1 and 1 inclusive)
- santorini_network_spec.md: contains a design document for messages sent over a network during a Santorini Tournament

The tests can be run by redirecting the X-in.json into xrun and using diff
with the output of xrun and the corresponding X-out.json

ex:
`./xrun < X-in.json | diff - X-out.json`

it should print nothing if the test is successful

There is also a TESTME script that can be run and it will print out the number of tests that passed/failed
