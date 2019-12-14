from itertools import repeat

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


def to_leaf_sweep_events_with_same_polygon_type(polygon_type: PolygonType
                                                ) -> Strategy[SweepEvent]:
    return strategies.builds(SweepEvent, booleans, points,
                             strategies.none(),
                             strategies.just(polygon_type), bound_edges_types)


leaf_sweep_events_with_same_polygon_type = (
    bound_polygons_types.flatmap(to_leaf_sweep_events_with_same_polygon_type))
leaf_sweep_events = strategies.builds(SweepEvent, booleans, points,
                                      strategies.none(),
                                      bound_polygons_types, bound_edges_types)


def to_sweep_events(leafs: Strategy[SweepEvent]) -> Strategy[SweepEvent]:
    acyclic_sweep_events = strategies.recursive(leafs,
                                                to_bound_sweep_events)
    return strategies.recursive(acyclic_sweep_events, make_cyclic)


sweep_events = to_sweep_events(leaf_sweep_events)
sweep_events_with_same_polygon_type = to_sweep_events(
        leaf_sweep_events_with_same_polygon_type)
events_queue_keys = strategies.builds(EventsQueueKey, sweep_events)
nested_sweep_events = to_bound_sweep_events(sweep_events)
nested_sweep_events_with_same_polygon_type = to_bound_sweep_events(
        sweep_events_with_same_polygon_type)
nested_events_queue_keys = strategies.builds(EventsQueueKey,
                                             nested_sweep_events)
totally_ordered_nested_events_queue_keys = strategies.builds(
        EventsQueueKey, nested_sweep_events_with_same_polygon_type)


def to_sweep_event_point(events_queue_key: EventsQueueKey) -> Point:
    return events_queue_key.event.point


totally_ordered_nested_events_queue_keys_triplets = (
        strategies.tuples(*repeat(totally_ordered_nested_events_queue_keys, 3))
        | strategies.lists(nested_events_queue_keys,
                           min_size=3,
                           max_size=3,
                           unique_by=to_sweep_event_point))
non_events_queue_keys = strategies.builds(object)
