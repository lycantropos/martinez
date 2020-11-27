from typing import Tuple

from hypothesis import given

from martinez.boolean import compute
from tests.port_tests.hints import (PortedOperationType,
                                    PortedPolygon)
from . import strategies


@given(strategies.polygons_pairs, strategies.operations_types)
def test_basic(polygons: Tuple[PortedPolygon, PortedPolygon],
               operation_type: PortedOperationType) -> None:
    left, right = polygons

    result = compute(left, right, operation_type)

    assert isinstance(result, PortedPolygon)
