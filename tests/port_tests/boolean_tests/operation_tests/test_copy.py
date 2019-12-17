import copy

from hypothesis import given

from martinez.boolean import Operation
from . import strategies


@given(strategies.operations)
def test_shallow(operation: Operation) -> None:
    result = copy.copy(operation)

    assert result is not operation
    assert result == operation
    assert result.left is operation.left
    assert result.right is operation.right


@given(strategies.operations)
def test_deep(operation: Operation) -> None:
    result = copy.deepcopy(operation)

    assert result is not operation
    assert result == operation
    assert result.left is not operation.left
    assert result.right is not operation.right
