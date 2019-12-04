import pickle

from _martinez import Point
from hypothesis import given

from . import strategies


@given(strategies.points)
def test_round_trip(point: Point) -> None:
    assert pickle.loads(pickle.dumps(point)) == point
