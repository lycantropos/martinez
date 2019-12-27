from _martinez import Operation
from hypothesis import given

from . import strategies


@given(strategies.operations)
def test_basic(operation: Operation) -> None:
    result = operation.run()

    assert result is None
