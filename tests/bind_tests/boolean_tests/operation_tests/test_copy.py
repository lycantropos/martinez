import copy

from _martinez import Operation
from hypothesis import given

from . import strategies


@given(strategies.operations)
def test_shallow(operation: Operation) -> None:
    result = copy.copy(operation)

    assert result is not operation
    assert result == operation


@given(strategies.operations)
def test_deep(operation: Operation) -> None:
    result = copy.deepcopy(operation)

    assert result is not operation
    assert result == operation
