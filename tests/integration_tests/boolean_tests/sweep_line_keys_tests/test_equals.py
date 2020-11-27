from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSweepLineKey
from tests.port_tests.hints import PortedSweepLineKey
from tests.utils import equivalence
from . import strategies


@given(strategies.sweep_line_keys_pairs, strategies.sweep_line_keys_pairs)
def test_basic(first_sweep_line_keys_pair: Tuple[BoundSweepLineKey,
                                                 PortedSweepLineKey],
               second_sweep_line_keys_pair: Tuple[BoundSweepLineKey,
                                                  PortedSweepLineKey]) -> None:
    first_bound, first_ported = first_sweep_line_keys_pair
    second_bound, second_ported = second_sweep_line_keys_pair

    assert equivalence(first_bound == second_bound,
                       first_ported == second_ported)
