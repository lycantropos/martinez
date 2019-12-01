from _martinez import BoundingBox as BoundBoundingBox
from hypothesis.searchstrategy import SearchStrategy

from martinez.bounding_box import BoundingBox as PortedBoundingBox

Strategy = SearchStrategy


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def are_bound_ported_bounding_boxes_equal(
        bound_bounding_box: BoundBoundingBox,
        ported_bounding_box: PortedBoundingBox) -> bool:
    return (bound_bounding_box.x_min == ported_bounding_box.x_min
            and bound_bounding_box.y_min == ported_bounding_box.y_min
            and bound_bounding_box.x_max == ported_bounding_box.x_max
            and bound_bounding_box.y_max == ported_bounding_box.y_max)
