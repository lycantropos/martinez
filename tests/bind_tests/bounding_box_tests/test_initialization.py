from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from . import strategies


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_basic(x_min: float, x_max: float, y_min: float, y_max: float) -> None:
    result = BoundBoundingBox(x_min, y_min, x_max, y_max)

    assert result.x_min == x_min
    assert result.y_min == y_min
    assert result.x_max == x_max
    assert result.y_max == y_max
