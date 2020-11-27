from hypothesis import given

from tests.bind_tests.hints import BoundOperation
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.operations)
def test_reflexivity(operation: BoundOperation) -> None:
    assert operation == operation


@given(strategies.operations, strategies.operations)
def test_symmetry(first_operation: BoundOperation,
                  second_operation: BoundOperation) -> None:
    assert equivalence(first_operation == second_operation,
                       second_operation == first_operation)


@given(strategies.operations, strategies.operations, strategies.operations)
def test_transitivity(first_operation: BoundOperation,
                      second_operation: BoundOperation,
                      third_operation: BoundOperation) -> None:
    assert implication(first_operation == second_operation
                       and second_operation == third_operation,
                       first_operation == third_operation)


@given(strategies.operations, strategies.operations)
def test_connection_with_inequality(first_operation: BoundOperation,
                                    second_operation: BoundOperation) -> None:
    assert equivalence(not first_operation == second_operation,
                       first_operation != second_operation)
