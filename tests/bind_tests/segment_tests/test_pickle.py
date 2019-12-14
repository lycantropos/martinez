from _martinez import Segment
from hypothesis import given

from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.segments)
def test_round_trip(segment: Segment) -> None:
    assert pickle_round_trip(segment) == segment
