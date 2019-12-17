import sys

from _martinez import Operation
from hypothesis import given

from . import strategies


@given(strategies.operations)
def test_basic(operation: Operation) -> None:
    result = repr(operation)

    assert result.startswith(Operation.__module__)
    assert Operation.__qualname__ in result


@given(strategies.operations)
def test_round_trip(operation: Operation) -> None:
    result = repr(operation)

    assert eval(result, sys.modules) == operation
