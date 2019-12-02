from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from tests.utils import are_bound_ported_points_equal
from . import strategies


@given(strategies.floats, strategies.floats)
def test_basic(x: float, y: float) -> None:
    bound, ported = Bound(x, y), Ported(x, y)

    assert are_bound_ported_points_equal(bound, ported)
