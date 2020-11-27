from hypothesis import given

from tests.bind_tests.hints import BoundPoint
from . import strategies


@given(strategies.floats, strategies.floats)
def test_basic(x: float, y: float) -> None:
    result = BoundPoint(x, y)

    assert result.x == x
    assert result.y == y
