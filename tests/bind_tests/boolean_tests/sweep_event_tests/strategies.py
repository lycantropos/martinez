from _martinez import (EdgeType,
                       Point,
                       PolygonType,
                       SweepEvent)
from hypothesis import strategies

from tests.strategies import (booleans,
                              floats,
                              unsigned_integers,
                              unsigned_integers_lists)

booleans = booleans
non_negative_integers = unsigned_integers
non_negative_integers_lists = unsigned_integers_lists
points = strategies.builds(Point, floats, floats)
polygons_types = strategies.sampled_from(list(PolygonType.__members__
                                              .values()))
edges_types = strategies.sampled_from(list(EdgeType.__members__.values()))
deferred_sweep_events = strategies.deferred(lambda: sweep_events)
maybe_sweep_events = strategies.none() | deferred_sweep_events
sweep_events = strategies.builds(SweepEvent, booleans, points,
                                 maybe_sweep_events,
                                 polygons_types, edges_types)
