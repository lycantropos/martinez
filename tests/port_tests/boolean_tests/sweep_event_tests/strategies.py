from functools import partial
from typing import Optional

from hypothesis import strategies

from martinez.boolean import (EdgeType,
                              PolygonType,
                              SweepEvent)
from martinez.hints import Scalar
from martinez.point import Point
from tests.strategies import (booleans,
                              make_cyclic,
                              scalars_strategies,
                              scalars_to_ported_points)
from tests.utils import Strategy

booleans = booleans
points = scalars_strategies.flatmap(scalars_to_ported_points)
polygons_types = strategies.sampled_from(list(PolygonType.__members__
                                              .values()))
edges_types = strategies.sampled_from(list(EdgeType.__members__.values()))


def to_sweep_events(scalars: Strategy[Scalar],
                    children: Strategy[Optional[SweepEvent]]
                    ) -> Strategy[SweepEvent]:
    return strategies.builds(SweepEvent, booleans,
                             strategies.builds(Point, scalars, scalars),
                             children, polygons_types, edges_types)


def scalars_to_leaf_sweep_events(scalars: Strategy[Scalar]
                                 ) -> Strategy[SweepEvent]:
    return strategies.builds(SweepEvent, booleans,
                             strategies.builds(Point, scalars, scalars),
                             strategies.none(), polygons_types, edges_types)


leaf_sweep_events = (scalars_strategies
                     .flatmap(partial(to_sweep_events,
                                      children=strategies.none())))


def scalars_to_sweep_events(scalars: Strategy[Scalar]) -> Strategy[SweepEvent]:
    return strategies.recursive(to_sweep_events(scalars, strategies.none()),
                                partial(to_sweep_events, scalars))


acyclic_sweep_events = scalars_strategies.flatmap(scalars_to_sweep_events)
sweep_events = strategies.recursive(acyclic_sweep_events, make_cyclic)
nested_sweep_events = (scalars_strategies
                       .flatmap(partial(to_sweep_events,
                                        children=sweep_events)))
maybe_sweep_events = strategies.none() | sweep_events
