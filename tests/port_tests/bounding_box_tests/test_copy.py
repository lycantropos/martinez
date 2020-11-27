import copy

from hypothesis import given

from tests.port_tests.hints import PortedBoundingBox
from . import strategies


@given(strategies.bounding_boxes)
def test_shallow(bounding_box: PortedBoundingBox) -> None:
    result = copy.copy(bounding_box)

    assert result is not bounding_box
    assert result == bounding_box


@given(strategies.bounding_boxes)
def test_deep(bounding_box: PortedBoundingBox) -> None:
    result = copy.deepcopy(bounding_box)

    assert result is not bounding_box
    assert result == bounding_box
