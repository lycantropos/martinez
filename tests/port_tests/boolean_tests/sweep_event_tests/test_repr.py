from hypothesis import given

from martinez import boolean
from martinez.boolean import SweepEvent
from . import strategies


@given(strategies.sweep_events)
def test_basic(event: SweepEvent) -> None:
    result = repr(event)

    assert result.startswith(SweepEvent.__qualname__)


@given(strategies.acyclic_sweep_events)
def test_round_trip(event: SweepEvent) -> None:
    result = repr(event)

    scalar_type = type(event.point.x)
    assert eval(result, {**vars(boolean),
                         scalar_type.__qualname__: scalar_type}) == event
