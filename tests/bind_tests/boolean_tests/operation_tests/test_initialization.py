from _martinez import (Operation,
                       OperationType,
                       Polygon)
from hypothesis import given

from . import strategies


@given(strategies.polygons, strategies.polygons, strategies.empty_polygons,
       strategies.operations_types)
def test_basic(left: Polygon, right: Polygon, resultant: Polygon,
               operation_type: OperationType) -> None:
    result = Operation(left, right, resultant, operation_type)

    assert result.left == left
    assert result.right == right
    assert result.resultant is resultant
    assert result.type == operation_type