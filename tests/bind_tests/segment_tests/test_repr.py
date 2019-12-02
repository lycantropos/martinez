import sys

from _martinez import Segment
from hypothesis import given

from . import strategies


@given(strategies.segments)
def test_basic(segment: Segment) -> None:
    result = repr(segment)

    assert result.startswith(Segment.__module__)
    assert Segment.__qualname__ in result


@given(strategies.segments)
def test_round_trip(segment: Segment) -> None:
    result = repr(segment)

    assert eval(result, sys.modules) == segment
