from typing import Optional

from _martinez import (EdgeType,
                       Point,
                       PolygonType,
                       SweepEvent)
from hypothesis import strategies

from tests.strategies import (booleans,
                              floats)
from tests.utils import Strategy

booleans = booleans
points = strategies.builds(Point, floats, floats)
polygons_types = strategies.sampled_from(list(PolygonType.__members__
                                              .values()))
edges_types = strategies.sampled_from(list(EdgeType.__members__.values()))


def extend_sweep_events(strategy: Strategy[Optional[SweepEvent]]
                        ) -> Strategy[SweepEvent]:
    def expand(sweep_event: Optional[SweepEvent]) -> Strategy[SweepEvent]:
        return strategies.builds(SweepEvent, booleans, points,
                                 strategies.just(sweep_event),
                                 polygons_types, edges_types)

    return strategy.flatmap(expand)


leaf_sweep_events = strategies.builds(SweepEvent, booleans, points,
                                      strategies.none(),
                                      polygons_types, edges_types)
sweep_events = strategies.recursive(leaf_sweep_events, extend_sweep_events)
maybe_sweep_events = strategies.none() | sweep_events
