from _martinez import (Operation,
                       Polygon)
from hypothesis import given

from . import strategies


@given(strategies.operations)
def test_basic(operation: Operation) -> None:
    assert isinstance(operation.resultant, Polygon)
