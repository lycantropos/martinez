from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from . import strategies


@given(strategies.operations)
def test_basic(operation: BoundOperation) -> None:
    assert isinstance(operation.is_trivial, bool)
