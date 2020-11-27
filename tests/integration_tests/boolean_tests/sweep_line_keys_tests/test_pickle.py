from typing import Tuple

from _martinez import SweepLineKey as Bound
from hypothesis import given

from martinez.boolean import SweepLineKey as Ported
from tests.utils import (pickle_round_trip)
from ...utils import are_bound_ported_sweep_line_keys_equal
from . import strategies


@given(strategies.sweep_line_keys_pairs)
def test_round_trip(sweep_line_keys_pair: Tuple[Bound, Ported]) -> None:
    bound, ported = sweep_line_keys_pair

    assert are_bound_ported_sweep_line_keys_equal(pickle_round_trip(bound),
                                                  pickle_round_trip(ported))
