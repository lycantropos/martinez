import pickle

from hypothesis import given

from martinez.point import Point
from . import strategies


@given(strategies.points)
def test_round_trip(point: Point) -> None:
    assert pickle.loads(pickle.dumps(point)) == point
