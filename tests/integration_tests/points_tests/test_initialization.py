from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from . import strategies


@given(strategies.floats, strategies.floats)
def test_basic(x: float, y: float) -> None:
    bound, ported = Bound(x, y), Ported(x, y)

    assert bound.x == ported.x
    assert bound.y == ported.y
