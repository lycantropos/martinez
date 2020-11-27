from hypothesis import given

from tests.bind_tests.hints import BoundSegment as BoundSegment
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.segments)
def test_round_trip(segment: BoundSegment) -> None:
    assert pickle_round_trip(segment) == segment
