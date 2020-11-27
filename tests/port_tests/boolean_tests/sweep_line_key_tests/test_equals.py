from typing import Tuple

from hypothesis import given

from tests.port_tests.hints import PortedSweepLineKey
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.sweep_line_keys)
def test_reflexivity(key: PortedSweepLineKey) -> None:
    assert key == key


@given(strategies.sweep_line_keys_pairs)
def test_symmetry(keys_pair: Tuple[PortedSweepLineKey, PortedSweepLineKey]
                  ) -> None:
    first_key, second_key = keys_pair

    assert equivalence(first_key == second_key, second_key == first_key)


@given(strategies.sweep_line_keys_triplets)
def test_transitivity(keys_triplet: Tuple[PortedSweepLineKey,
                                          PortedSweepLineKey,
                                          PortedSweepLineKey]) -> None:
    first_key, second_key, third_key = keys_triplet

    assert implication(first_key == second_key and second_key == third_key,
                       first_key == third_key)


@given(strategies.sweep_line_keys_pairs)
def test_connection_with_inequality(keys_pair: Tuple[PortedSweepLineKey,
                                                     PortedSweepLineKey]
                                    ) -> None:
    first_key, second_key = keys_pair

    assert equivalence(not first_key == second_key,
                       first_key != second_key)
