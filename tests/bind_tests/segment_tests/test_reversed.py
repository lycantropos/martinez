from hypothesis import given

from tests.bind_tests.hints import BoundSegment
from . import strategies


@given(strategies.segments)
def test_basic(segment: BoundSegment) -> None:
    assert isinstance(segment.reversed, BoundSegment)


@given(strategies.segments)
def test_involution(segment: BoundSegment) -> None:
    assert segment.reversed.reversed == segment
