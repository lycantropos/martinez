from typing import Optional

from _martinez import (EdgeType,
                       Point,
                       PolygonType,
                       SweepEvent)
from hypothesis import strategies

from tests.strategies import (booleans,
                              floats,
                              unsigned_integers,
                              unsigned_integers_lists)
from tests.utils import Strategy

booleans = booleans
non_negative_integers = unsigned_integers
non_negative_integers_lists = unsigned_integers_lists
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


sweep_events = strategies.recursive(strategies.builds(SweepEvent, booleans,
                                                      points,
                                                      strategies.none(),
                                                      polygons_types,
                                                      edges_types),
                                    extend_sweep_events)
maybe_sweep_events = strategies.none() | sweep_events
