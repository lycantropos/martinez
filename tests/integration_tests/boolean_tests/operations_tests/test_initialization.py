from typing import Tuple

from _martinez import (Operation as Bound,
                       OperationType as BoundOperationType,
                       Polygon as BoundPolygon)
from hypothesis import given

from martinez.boolean import (Operation as Ported,
                              OperationType as PortedOperationType)
from martinez.polygon import Polygon as PortedPolygon
from tests.utils import are_bound_ported_operations_equal
from . import strategies


@given(strategies.bound_with_ported_polygons_pairs,
       strategies.bound_with_ported_polygons_pairs,
       strategies.bound_with_ported_operations_types_pairs)
def test_basic(
        bound_with_ported_left_polygons_pair: Tuple[BoundPolygon,
                                                    PortedPolygon],
        bound_with_ported_right_polygons_pair: Tuple[BoundPolygon,
                                                     PortedPolygon],
        bound_with_ported_operations_types_pair: Tuple[BoundOperationType,
                                                       PortedOperationType],
) -> None:
    bound_left, ported_left = bound_with_ported_left_polygons_pair
    bound_right, ported_right = bound_with_ported_right_polygons_pair
    (bound_operation_type,
     ported_operation_type) = bound_with_ported_operations_types_pair

    bound = Bound(bound_left, bound_right,  bound_operation_type)
    ported = Ported(ported_left, ported_right, ported_operation_type)

    assert are_bound_ported_operations_equal(bound, ported)
