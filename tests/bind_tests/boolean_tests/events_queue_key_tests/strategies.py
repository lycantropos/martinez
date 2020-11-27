from itertools import repeat
from typing import Hashable

from _martinez import (EventsQueueKey,
                       PolygonType,
                       SweepEvent)
from hypothesis import strategies

from tests.strategies import (booleans,
                              bound_polygons_types)
from tests.bind_tests.factories import to_bound_sweep_events, \
    to_nested_bound_sweep_events
from tests.utils import Strategy

booleans = booleans

sweep_events = to_bound_sweep_events()


def to_nested_sweep_events_with_same_polygon_type(polygon_type: PolygonType
                                                  ) -> Strategy[SweepEvent]:
    return to_nested_bound_sweep_events(
            polygons_types=strategies.just(polygon_type))


nested_sweep_events_with_same_polygon_type = bound_polygons_types.flatmap(
        to_nested_sweep_events_with_same_polygon_type)
events_queue_keys = strategies.builds(EventsQueueKey, sweep_events)
nested_sweep_events = to_nested_bound_sweep_events()
nested_events_queue_keys = strategies.builds(EventsQueueKey,
                                             nested_sweep_events)
totally_ordered_nested_events_queue_keys = strategies.builds(
        EventsQueueKey, nested_sweep_events_with_same_polygon_type)


def to_sweep_event_point(key: EventsQueueKey) -> Hashable:
    point = key.event.point
    return point.x, point.y


totally_ordered_nested_events_queue_keys_triplets = (
        strategies.tuples(*repeat(totally_ordered_nested_events_queue_keys, 3))
        | strategies.lists(nested_events_queue_keys,
                           min_size=3,
                           max_size=3,
                           unique_by=to_sweep_event_point))
non_events_queue_keys = strategies.builds(object)
