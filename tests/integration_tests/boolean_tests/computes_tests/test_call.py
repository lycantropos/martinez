from typing import Tuple

from _martinez import (OperationType as BoundOperationType,
                       Polygon as BoundPolygon,
                       compute as bound)
from hypothesis import given

from martinez.boolean import (OperationType as PortedOperationType,
                              Polygon as PortedPolygon,
                              compute as ported)
from tests.integration_tests.utils import are_bound_ported_polygons_equal
from . import strategies


@given(strategies.polygons_pairs_pairs, strategies.operations_types_pairs)
def test_basic(polygons_pairs_pair: Tuple[Tuple[BoundPolygon, PortedPolygon],
                                          Tuple[BoundPolygon, PortedPolygon]],
               operations_types_pair: Tuple[BoundOperationType,
                                            PortedOperationType]) -> None:
    ((bound_left, ported_left),
     (bound_right, ported_right)) = polygons_pairs_pair
    bound_operation_type, ported_operation_type = operations_types_pair

    bound_result = bound(bound_left, bound_right, bound_operation_type)
    ported_result = ported(ported_left, ported_right, ported_operation_type)

    assert are_bound_ported_polygons_equal(bound_result, ported_result)
