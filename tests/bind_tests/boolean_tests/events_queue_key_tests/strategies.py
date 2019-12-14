from _martinez import (EventsQueueKey,
                       Point,
                       PolygonType,
                       SweepEvent)
from hypothesis import strategies

from tests.strategies import (booleans,
                              bound_edges_types,
                              bound_polygons_types,
                              floats,
                              make_cyclic,
                              to_bound_sweep_events)
from tests.utils import Strategy

booleans = booleans
points = strategies.builds(Point, floats, floats)
polygons_types = bound_polygons_types
edges_types = bound_edges_types


def to_sweep_events_with_same_polygon_type(polygon_type: PolygonType
                                           ) -> Strategy[SweepEvent]:
    return strategies.builds(SweepEvent, booleans, points,
                             strategies.none(),
                             strategies.just(polygon_type), bound_edges_types)


leaf_sweep_events = (bound_polygons_types
                     .flatmap(to_sweep_events_with_same_polygon_type))
acyclic_sweep_events = strategies.recursive(leaf_sweep_events,
                                            to_bound_sweep_events)
sweep_events = strategies.recursive(acyclic_sweep_events, make_cyclic)
events_queue_keys = strategies.builds(EventsQueueKey, sweep_events)
nested_sweep_events = to_bound_sweep_events(sweep_events)
nested_events_queue_keys = strategies.builds(EventsQueueKey,
                                             nested_sweep_events)
non_events_queue_keys = strategies.builds(object)
