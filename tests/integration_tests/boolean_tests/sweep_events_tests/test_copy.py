import copy
from typing import Tuple

from hypothesis import given

from tests.bind_tests.hints import BoundSweepEvent
from tests.integration_tests.utils import are_bound_ported_sweep_events_equal
from tests.port_tests.hints import PortedSweepEvent
from . import strategies


@given(strategies.sweep_events_pairs)
def test_shallow(sweep_events_pair: Tuple[BoundSweepEvent, PortedSweepEvent]
                 ) -> None:
    bound, ported = sweep_events_pair

    assert are_bound_ported_sweep_events_equal(copy.copy(bound),
                                               copy.copy(ported))


@given(strategies.sweep_events_pairs)
def test_deep(sweep_events_pair: Tuple[BoundSweepEvent, PortedSweepEvent]
              ) -> None:
    bound, ported = sweep_events_pair

    assert are_bound_ported_sweep_events_equal(copy.deepcopy(bound),
                                               copy.deepcopy(ported))
