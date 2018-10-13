from strategy import Strategy
from turn_strategy import TurnStrategy
from placement_strategy import PlacementStrategy

"""
A ModularStrategy object is a Strategy that uses a TurnStrategy and PlacementStrategy
to determine turns and worker placements.
"""
def ModularStrategy(Strategy):
    """
    Takes a TurnStrategy and a PlacementStrategy to make move decisions
    @turn_strategy: a TurnStrategy to use
    @placement_strategy: a PlacmentStrategy to use
    """
    def __init__(self, turn_strategy: TurnStrategy, placement_strategy: PlacementStrategy):
        pass
