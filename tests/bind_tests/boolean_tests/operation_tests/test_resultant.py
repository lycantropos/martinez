from hypothesis import given

from tests.bind_tests.hints import (BoundOperation,
                                    BoundPolygon)
from . import strategies


@given(strategies.operations)
def test_basic(operation: BoundOperation) -> None:
    assert isinstance(operation.resultant, BoundPolygon)
