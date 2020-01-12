from _martinez import SweepLineKey
from hypothesis import given

from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.sweep_line_keys)
def test_reflexivity(key: SweepLineKey) -> None:
    assert key == key


@given(strategies.sweep_line_keys, strategies.sweep_line_keys)
def test_symmetry(first_key: SweepLineKey, second_key: SweepLineKey) -> None:
    assert equivalence(first_key == second_key, second_key == first_key)


@given(strategies.sweep_line_keys, strategies.sweep_line_keys,
       strategies.sweep_line_keys)
def test_transitivity(first_key: SweepLineKey,
                      second_key: SweepLineKey,
                      third_key: SweepLineKey) -> None:
    assert implication(first_key == second_key and second_key == third_key,
                       first_key == third_key)


@given(strategies.sweep_line_keys, strategies.sweep_line_keys)
def test_connection_with_inequality(first_key: SweepLineKey,
                                    second_key: SweepLineKey) -> None:
    assert equivalence(not first_key == second_key, first_key != second_key)
