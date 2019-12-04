import pickle

from _martinez import Segment
from hypothesis import given

from . import strategies


@given(strategies.segments)
def test_round_trip(segment: Segment) -> None:
    assert pickle.loads(pickle.dumps(segment)) == segment
