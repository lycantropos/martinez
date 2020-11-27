from hypothesis import given

from tests.port_tests.hints import PortedBoundingBox
from . import strategies


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_basic(first_bounding_box: PortedBoundingBox,
               second_bounding_box: PortedBoundingBox) -> None:
    result = first_bounding_box + second_bounding_box

    assert isinstance(result, PortedBoundingBox)


@given(strategies.bounding_boxes)
def test_idempotence(bounding_box: PortedBoundingBox) -> None:
    assert bounding_box + bounding_box == bounding_box


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_commutativity(first_bounding_box: PortedBoundingBox,
                       second_bounding_box: PortedBoundingBox) -> None:
    assert (first_bounding_box + second_bounding_box
            == second_bounding_box + first_bounding_box)


@given(strategies.bounding_boxes,
       strategies.bounding_boxes,
       strategies.bounding_boxes)
def test_associativity(first_bounding_box: PortedBoundingBox,
                       second_bounding_box: PortedBoundingBox,
                       third_bounding_box: PortedBoundingBox) -> None:
    assert ((first_bounding_box + second_bounding_box) + third_bounding_box
            == first_bounding_box + (second_bounding_box + third_bounding_box))
