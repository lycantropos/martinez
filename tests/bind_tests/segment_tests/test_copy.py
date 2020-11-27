import copy

from hypothesis import given

from tests.bind_tests.hints import BoundSegment as BoundSegment
from . import strategies


@given(strategies.segments)
def test_shallow(segment: BoundSegment) -> None:
    result = copy.copy(segment)

    assert result is not segment
    assert result == segment


@given(strategies.segments)
def test_deep(segment: BoundSegment) -> None:
    result = copy.deepcopy(segment)

    assert result is not segment
    assert result == segment
