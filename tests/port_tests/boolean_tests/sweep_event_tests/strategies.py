from typing import Optional

from hypothesis import strategies

from martinez.boolean import (EdgeType,
                              PolygonType,
                              SweepEvent)
from martinez.hints import Scalar
from martinez.point import Point
from tests.strategies import (booleans, scalars_strategies,
                              scalars_to_ported_points)
from tests.utils import Strategy

booleans = booleans
points = scalars_strategies.flatmap(scalars_to_ported_points)
polygons_types = strategies.sampled_from(list(PolygonType.__members__
                                              .values()))
edges_types = strategies.sampled_from(list(EdgeType.__members__.values()))


def scalars_to_sweep_events(scalars: Strategy[Scalar]) -> Strategy[SweepEvent]:
    def from_children(children: Strategy[Optional[SweepEvent]]
                      ) -> Strategy[SweepEvent]:
        return strategies.builds(SweepEvent, booleans,
                                 strategies.builds(Point, scalars, scalars),
                                 children, polygons_types, edges_types)

    return strategies.recursive(from_children(strategies.none()),
                                from_children)


sweep_events = scalars_strategies.flatmap(scalars_to_sweep_events)
maybe_sweep_events = strategies.none() | sweep_events
