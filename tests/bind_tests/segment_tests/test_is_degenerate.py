from _martinez import Segment
from hypothesis import given

from . import strategies


@given(strategies.segments)
def test_basic(segment: Segment) -> None:
    result = segment.is_degenerate

    assert isinstance(result, bool)
