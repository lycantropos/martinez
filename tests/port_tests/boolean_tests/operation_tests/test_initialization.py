from hypothesis import given

from martinez.boolean import (Operation,
                              OperationType)
from martinez.polygon import Polygon
from . import strategies


@given(strategies.polygons, strategies.polygons, strategies.operations_types)
def test_basic(left: Polygon, right: Polygon,
               operation_type: OperationType) -> None:
    result = Operation(left, right, operation_type)

    assert result.left == left
    assert result.right == right
    assert result.type == operation_type
