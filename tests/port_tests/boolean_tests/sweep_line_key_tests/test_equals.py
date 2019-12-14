from hypothesis import given

from martinez.boolean import SweepLineKey
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.sweep_line_keys)
def test_reflexivity(sweep_line_key: SweepLineKey) -> None:
    assert sweep_line_key == sweep_line_key


@given(strategies.sweep_line_keys, strategies.sweep_line_keys)
def test_symmetry(first_sweep_line_key: SweepLineKey,
                  second_sweep_line_key: SweepLineKey) -> None:
    assert equivalence(first_sweep_line_key == second_sweep_line_key,
                       second_sweep_line_key == first_sweep_line_key)


@given(strategies.sweep_line_keys,
       strategies.sweep_line_keys,
       strategies.sweep_line_keys)
def test_transitivity(first_sweep_line_key: SweepLineKey,
                      second_sweep_line_key: SweepLineKey,
                      third_sweep_line_key: SweepLineKey) -> None:
    assert implication(first_sweep_line_key == second_sweep_line_key
                       and second_sweep_line_key == third_sweep_line_key,
                       first_sweep_line_key == third_sweep_line_key)


@given(strategies.sweep_line_keys, strategies.sweep_line_keys)
def test_connection_with_inequality(first_sweep_line_key: SweepLineKey,
                                    second_sweep_line_key: SweepLineKey
                                    ) -> None:
    assert equivalence(not first_sweep_line_key == second_sweep_line_key,
                       first_sweep_line_key != second_sweep_line_key)
