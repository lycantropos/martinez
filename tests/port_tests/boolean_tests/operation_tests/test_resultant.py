from hypothesis import given

from tests.port_tests.hints import (PortedOperation,
                                    PortedPolygon)
from . import strategies


@given(strategies.operations)
def test_basic(operation: PortedOperation) -> None:
    assert isinstance(operation.resultant, PortedPolygon)
