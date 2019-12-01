from _martinez import Point as Bound
from hypothesis import given

from martinez.point import Point as Ported
from tests import strategies
from tests.utils import (equivalence,
                         implication)


@given(strategies.floats, strategies.floats)
def test_reflexivity(x: float, y: float) -> None:
    bound, ported = Bound(x, y), Ported(x, y)

    assert equivalence(bound == bound, ported == ported)


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_symmetry(first_x: float, first_y: float,
                  second_x: float, second_y: float) -> None:
    first_bound, second_bound = (Bound(first_x, first_y),
                                 Bound(second_x, second_y))
    first_ported, second_ported = (Ported(first_x, first_y),
                                   Ported(second_x, second_y))

    assert equivalence(equivalence(first_bound == second_bound,
                                   second_bound == first_bound),
                       equivalence(first_ported == second_ported,
                                   second_ported == first_ported))


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_transitivity(first_x: float, first_y: float,
                      second_x: float, second_y: float,
                      third_x: float, third_y: float) -> None:
    first_bound, second_bound, third_bound = (Bound(first_x, first_y),
                                              Bound(second_x, second_y),
                                              Bound(third_x, third_y))
    first_ported, second_ported, third_ported = (Ported(first_x, first_y),
                                                 Ported(second_x, second_y),
                                                 Ported(third_x, third_y))

    assert equivalence(implication(first_bound == second_bound
                                   and second_bound == third_bound,
                                   first_bound == third_bound),
                       implication(first_ported == second_ported
                                   and second_ported == third_ported,
                                   first_ported == third_ported))


@given(strategies.floats, strategies.floats,
       strategies.floats, strategies.floats)
def test_connection_with_inequality(first_x: float, first_y: float,
                                    second_x: float, second_y: float) -> None:
    first_bound, second_bound = (Bound(first_x, first_y),
                                 Bound(second_x, second_y))
    first_ported, second_ported = (Ported(first_x, first_y),
                                   Ported(second_x, second_y))

    assert equivalence(equivalence(not first_bound == second_bound,
                                   first_bound != second_bound),
                       equivalence(not first_ported == second_ported,
                                   first_ported != second_ported))
