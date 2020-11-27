from hypothesis import given

from tests.bind_tests.hints import BoundSegment
from . import strategies


@given(strategies.segments)
def test_basic(segment: BoundSegment) -> None:
    result = segment.is_degenerate

    assert isinstance(result, bool)
