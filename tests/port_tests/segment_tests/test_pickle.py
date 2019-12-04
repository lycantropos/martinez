import pickle

from hypothesis import given

from martinez.segment import Segment
from . import strategies


@given(strategies.segments)
def test_round_trip(segment: Segment) -> None:
    assert pickle.loads(pickle.dumps(segment)) == segment
