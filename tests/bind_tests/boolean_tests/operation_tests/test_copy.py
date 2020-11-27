import copy

from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from . import strategies


@given(strategies.operations)
def test_shallow(operation: BoundOperation) -> None:
    result = copy.copy(operation)

    assert result is not operation
    assert result == operation


@given(strategies.operations)
def test_deep(operation: BoundOperation) -> None:
    result = copy.deepcopy(operation)

    assert result is not operation
    assert result == operation
