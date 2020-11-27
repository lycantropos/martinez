from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundOperationType,
                                    BoundPolygon)
from tests.integration_tests.utils import are_bound_ported_operations_equal
from tests.port_tests.hints import (PortedOperation,
                                    PortedOperationType,
                                    PortedPolygon)
from . import strategies


@given(strategies.polygons_pairs, strategies.polygons_pairs,
       strategies.operations_types_pairs)
def test_basic(left_polygons_pair: Tuple[BoundPolygon, PortedPolygon],
               right_polygons_pair: Tuple[BoundPolygon, PortedPolygon],
               operations_types_pair: Tuple[BoundOperationType,
                                            PortedOperationType]) -> None:
    bound_left, ported_left = left_polygons_pair
    bound_right, ported_right = right_polygons_pair
    bound_operation_type, ported_operation_type = operations_types_pair

    bound = BoundOperation(bound_left, bound_right, bound_operation_type)
    ported = PortedOperation(ported_left, ported_right, ported_operation_type)

    assert are_bound_ported_operations_equal(bound, ported)
