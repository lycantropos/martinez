from typing import Tuple

from hypothesis import given

from martinez.boolean import (OperationType,
                              compute)
from martinez.polygon import Polygon
from . import strategies


@given(strategies.polygons_pairs, strategies.operations_types)
def test_basic(polygons: Tuple[Polygon, Polygon],
               operation_type: OperationType) -> None:
    left, right = polygons

    result = compute(left, right, operation_type)

    assert isinstance(result, Polygon)
