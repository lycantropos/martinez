from hypothesis import given

from tests.bind_tests.hints import BoundSegment as BoundSegment
from . import strategies


@given(strategies.segments)
def test_basic(segment: BoundSegment) -> None:
    result = segment.is_vertical

    assert isinstance(result, bool)
