import sys

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from . import strategies


@given(strategies.operations)
def test_basic(operation: BoundOperation) -> None:
    result = repr(operation)

    assert result.startswith(BoundOperation.__module__)
    assert BoundOperation.__qualname__ in result


@given(strategies.operations)
def test_round_trip(operation: BoundOperation) -> None:
    result = repr(operation)

    assert eval(result, sys.modules) == operation
