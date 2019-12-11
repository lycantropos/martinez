from typing import Optional

from _martinez import (EdgeType,
                       Point,
                       PolygonType,
                       SweepEvent)
from hypothesis import strategies

from tests.strategies import (booleans,
                              floats,
                              make_cyclic)
from tests.utils import Strategy

booleans = booleans
points = strategies.builds(Point, floats, floats)
polygons_types = strategies.sampled_from(list(PolygonType.__members__
                                              .values()))
edges_types = strategies.sampled_from(list(EdgeType.__members__.values()))
leaf_sweep_events = strategies.builds(SweepEvent, booleans, points,
                                      strategies.none(),
                                      polygons_types, edges_types)


def to_sweep_events(children: Strategy[Optional[SweepEvent]]
                    ) -> Strategy[SweepEvent]:
    return strategies.builds(SweepEvent, booleans, points,
                             children, polygons_types, edges_types)


acyclic_sweep_events = strategies.recursive(leaf_sweep_events, to_sweep_events)
sweep_events = strategies.recursive(acyclic_sweep_events, make_cyclic)
nested_sweep_events = to_sweep_events(sweep_events)
maybe_sweep_events = strategies.none() | sweep_events
