from functools import partial
from itertools import repeat
from typing import (Any,
                    List,
                    Optional)

from hypothesis import strategies

from tests.strategies import (booleans,
                              floats,
                              unsigned_integers)
from tests.utils import (MAX_NESTING_DEPTH,
                         Strategy,
                         compose,
                         make_cyclic,
                         to_valid_coordinates_pairs)
from .hints import (BoundContour,
                    BoundPoint,
                    BoundPolygonType,
                    BoundSweepEvent)
from .utils import (bound_edges_types,
                    bound_polygons_types,
                    to_bound_rectangle)


def to_bound_contours(coordinates: Strategy[float] = floats,
                      *,
                      holes: Strategy[List[int]] = strategies.builds(list),
                      are_external: Strategy[bool] = strategies.just(True)
                      ) -> Strategy[BoundContour]:
    coordinates = (strategies.lists(coordinates,
                                    min_size=2)
                   .map(sorted)
                   .map(to_valid_coordinates_pairs))
    rectangles_vertices = strategies.builds(to_bound_rectangle,
                                            coordinates, coordinates)
    contours_vertices = rectangles_vertices
    return strategies.builds(BoundContour,
                             contours_vertices, holes, are_external)


def to_plain_bound_sweep_events(
        children: Strategy[Optional[BoundSweepEvent]],
        *,
        polygons_types: Strategy[BoundPolygonType] = bound_polygons_types
) -> Strategy[BoundSweepEvent]:
    return strategies.builds(BoundSweepEvent, booleans,
                             strategies.builds(BoundPoint, floats, floats),
                             children, polygons_types, bound_edges_types,
                             booleans, booleans, booleans, booleans,
                             unsigned_integers, unsigned_integers, children)


def to_bound_sweep_events(*,
                          min_depth: int = 1,
                          max_depth: int = MAX_NESTING_DEPTH,
                          **kwargs: Any) -> Strategy[BoundSweepEvent]:
    acyclic_events = to_acyclic_bound_sweep_events(min_depth=min_depth,
                                                   max_depth=max_depth,
                                                   **kwargs)
    return make_cyclic(acyclic_events)


def to_acyclic_bound_sweep_events(*,
                                  min_depth: int = 1,
                                  max_depth: int = MAX_NESTING_DEPTH,
                                  **kwargs: Any) -> Strategy[BoundSweepEvent]:
    events_factory = partial(to_plain_bound_sweep_events, **kwargs)
    base = compose(*repeat(events_factory,
                           times=min_depth))(strategies.none())
    return strategies.recursive(base, events_factory,
                                max_leaves=max_depth - min_depth)


to_nested_bound_sweep_events = partial(to_bound_sweep_events,
                                       min_depth=2)
