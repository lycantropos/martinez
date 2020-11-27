from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSweepLineKey
from tests.integration_tests.utils import (
    are_bound_ported_sweep_line_keys_equal)
from tests.port_tests.hints import PortedSweepLineKey
from tests.utils import pickle_round_trip
from . import strategies


@given(strategies.sweep_line_keys_pairs)
def test_round_trip(sweep_line_keys_pair: Tuple[BoundSweepLineKey,
                                                PortedSweepLineKey]) -> None:
    bound, ported = sweep_line_keys_pair

    assert are_bound_ported_sweep_line_keys_equal(pickle_round_trip(bound),
                                                  pickle_round_trip(ported))
