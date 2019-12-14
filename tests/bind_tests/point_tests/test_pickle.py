from _martinez import Point
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.points)
def test_round_trip(point: Point) -> None:
    assert pickle_round_trip(point) == point
