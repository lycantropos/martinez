from hypothesis import given

from martinez.boolean import Operation
from . import strategies


@given(strategies.operations)
def test_basic(operation: Operation) -> None:
    assert isinstance(operation.is_trivial, bool)
