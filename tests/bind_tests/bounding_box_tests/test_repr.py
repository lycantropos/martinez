import sys

from hypothesis import given

from tests.bind_tests.hints import BoundBoundingBox
from . import strategies


@given(strategies.bounding_boxes)
def test_basic(bounding_box: BoundBoundingBox) -> None:
    result = repr(bounding_box)

    assert result.startswith(BoundBoundingBox.__module__)
    assert BoundBoundingBox.__qualname__ in result


@given(strategies.bounding_boxes)
def test_round_trip(bounding_box: BoundBoundingBox) -> None:
    result = repr(bounding_box)

    assert eval(result, sys.modules) == bounding_box
