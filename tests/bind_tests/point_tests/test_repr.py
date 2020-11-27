import sys

from hypothesis import given

from tests.bind_tests.hints import BoundPoint as BoundPoint
from . import strategies


@given(strategies.points)
def test_basic(point: BoundPoint) -> None:
    result = repr(point)

    assert result.startswith(BoundPoint.__module__)
    assert BoundPoint.__qualname__ in result


@given(strategies.points)
def test_round_trip(point: BoundPoint) -> None:
    result = repr(point)

    assert eval(result, sys.modules) == point
