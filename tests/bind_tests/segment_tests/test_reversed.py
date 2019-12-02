from _martinez import Segment
from hypothesis import given

from . import strategies


@given(strategies.segments)
def test_basic(segment: Segment) -> None:
    assert isinstance(segment.reversed, Segment)


@given(strategies.segments)
def test_involution(segment: Segment) -> None:
    assert segment.reversed.reversed == segment
