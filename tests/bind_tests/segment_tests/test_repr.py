import sys

from hypothesis import given

from tests.bind_tests.hints import BoundSegment
from . import strategies


@given(strategies.segments)
def test_basic(segment: BoundSegment) -> None:
    result = repr(segment)

    assert result.startswith(BoundSegment.__module__)
    assert BoundSegment.__qualname__ in result


@given(strategies.segments)
def test_round_trip(segment: BoundSegment) -> None:
    result = repr(segment)

    assert eval(result, sys.modules) == segment
