from hypothesis import given

from tests.port_tests.hints import (PortedOperation,
                                    PortedOperationType,
                                    PortedPolygon)
from . import strategies


@given(strategies.polygons, strategies.polygons, strategies.operations_types)
def test_basic(left: PortedPolygon,
               right: PortedPolygon,
               operation_type: PortedOperationType) -> None:
    result = PortedOperation(left, right, operation_type)

    assert result.left == left
    assert result.right == right
    assert result.type == operation_type
