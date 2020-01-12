from typing import Tuple

from hypothesis import given

from martinez.boolean import Operation
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.operations)
def test_reflexivity(operation: Operation) -> None:
    assert operation == operation


@given(strategies.operations_pairs)
def test_symmetry(operations_pair: Tuple[Operation, Operation]) -> None:
    first_operation, second_operation = operations_pair

    assert equivalence(first_operation == second_operation,
                       second_operation == first_operation)


@given(strategies.operations_triplets)
def test_transitivity(operations_triplet: Tuple[Operation, Operation,
                                                Operation]) -> None:
    first_operation, second_operation, third_operation = operations_triplet

    assert implication(first_operation == second_operation
                       and second_operation == third_operation,
                       first_operation == third_operation)


@given(strategies.operations_pairs)
def test_connection_with_inequality(operations_pair: Tuple[Operation,
                                                           Operation]) -> None:
    first_operation, second_operation = operations_pair

    assert equivalence(not first_operation == second_operation,
                       first_operation != second_operation)
