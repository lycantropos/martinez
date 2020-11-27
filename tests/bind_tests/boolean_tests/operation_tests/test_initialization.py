from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundOperationType,
                                    BoundPolygon)
from . import strategies


@given(strategies.polygons, strategies.polygons, strategies.operations_types)
def test_basic(left: BoundPolygon,
               right: BoundPolygon,
               operation_type: BoundOperationType) -> None:
    result = BoundOperation(left, right, operation_type)

    assert result.left == left
    assert result.right == right
    assert result.type == operation_type
