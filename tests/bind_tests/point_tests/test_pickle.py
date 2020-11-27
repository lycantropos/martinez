from hypothesis import given

from tests.bind_tests.hints import BoundPoint as BoundPoint
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.points)
def test_round_trip(point: BoundPoint) -> None:
    assert pickle_round_trip(point) == point
