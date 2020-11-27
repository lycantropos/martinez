from hypothesis import given

from tests.port_tests.hints import PortedBoundingBox
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.bounding_boxes)
def test_reflexivity(bounding_box: PortedBoundingBox) -> None:
    assert bounding_box == bounding_box


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_symmetry(first_bounding_box: PortedBoundingBox,
                  second_bounding_box: PortedBoundingBox) -> None:
    assert equivalence(first_bounding_box == second_bounding_box,
                       second_bounding_box == first_bounding_box)


@given(strategies.bounding_boxes, strategies.bounding_boxes,
       strategies.bounding_boxes)
def test_transitivity(first_bounding_box: PortedBoundingBox,
                      second_bounding_box: PortedBoundingBox,
                      third_bounding_box: PortedBoundingBox) -> None:
    assert implication(first_bounding_box == second_bounding_box
                       and second_bounding_box == third_bounding_box,
                       first_bounding_box == third_bounding_box)


@given(strategies.bounding_boxes, strategies.bounding_boxes)
def test_connection_with_inequality(first_bounding_box: PortedBoundingBox,
                                    second_bounding_box: PortedBoundingBox) -> None:
    assert equivalence(not first_bounding_box == second_bounding_box,
                       first_bounding_box != second_bounding_box)
