from typing import Tuple

from _martinez import compute
from hypothesis import given

from tests.bind_tests.hints import (BoundOperationType,
                                    BoundPolygon)
from . import strategies


@given(strategies.polygons_pairs, strategies.operations_types)
def test_basic(polygons: Tuple[BoundPolygon, BoundPolygon],
               operation_type: BoundOperationType) -> None:
    left, right = polygons

    result = compute(left, right, operation_type)

    assert isinstance(result, BoundPolygon)
