from typing import Tuple

from _martinez import (OperationType,
                       Polygon,
                       compute)
from hypothesis import given

from . import strategies


@given(strategies.polygons_pairs, strategies.operations_types)
def test_basic(polygons: Tuple[Polygon, Polygon],
               operation_type: OperationType) -> None:
    left, right = polygons

    result = compute(left, right, operation_type)

    assert isinstance(result, Polygon)
