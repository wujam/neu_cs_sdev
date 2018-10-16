# 7
## Files
- aux: folder for auxillary files
  - parse_json.py: library file to parse json objects from a string
- xrules: systems level test harness for the strategy implementation
- strategy-tests: contains sample input and outputs to use with xstrategy
  - X-in.json (X between 1 and 2 inclusive)
  - X-out.json (X between 1 and 2 inclusive)

The tests can be run by redirecting the X-in.json into xstrategy and using diff
with the output of xstrategy and the corresponding X-out.json

ex:
`./xstrategy < X-in.json | diff - X-out.json`

it should print nothing if the test is successful

-Santorini/Design/strategy.py: Design for a Strategy interface whose job is to determine the best next move
-Santorini/Design/modular_strategy.py: Design for a ModularStrategy interface that implements the Strategy interface by taking a TurnStrategy object and PlacementStrategy object
-Santorini/Design/placement_strategy.py: Design for a PlacementStrategy interface that determines the best placement for the next worker
-Santorini/Design/turn_strategy.py: Design for a TurnStrategy interface that determines the best turn to take
-Santorini/Design/referee.py: Design for a Referee component that oversees a game and regulates players, moves, and the board to play out a game.

-Santorini/Common/modular_strategy.py: ModularStrategy implementation that uses a PlacementStrategy and TurnStrategy to determine placements and moves
-Santorini/Common/diagonal_placement_strategy.py: PlacementStrategy that aims to place next workers on the next spot on the x=y diagonal
-Santorini/Common/far_away_placement_strategy.py: PlacementStrategy that aims to place next workers on the furthest spot from opposing workers
-Santorini/Common/turn_strategy.py: TurnStrategy that aims to stay alive for the given number of lookaheads, or take a winning move if possible, or determine if all moves lead to death
-Santorini/Common/test_{COMPONENT_NAME}.py: unit tests for the module named COMPONENT_NAME
