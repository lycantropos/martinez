from typing import Tuple

from _martinez import Operation as Bound
from hypothesis import given

from martinez.boolean import Operation as Ported
from ...utils import are_bound_ported_polygons_equal
from . import strategies


@given(strategies.operations_pairs)
def test_basic(operations_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = operations_pair

    assert bound.is_trivial is ported.is_trivial
    assert are_bound_ported_polygons_equal(bound.resultant, ported.resultant)
