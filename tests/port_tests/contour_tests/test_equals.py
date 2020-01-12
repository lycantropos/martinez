from typing import Tuple

from hypothesis import given

from martinez.contour import Contour
from tests.utils import (equivalence,
                         implication)
from . import strategies


@given(strategies.contours)
def test_reflexivity(contour: Contour) -> None:
    assert contour == contour


@given(strategies.contours_pairs)
def test_symmetry(contours_pair: Tuple[Contour, Contour]) -> None:
    first_contour, second_contour = contours_pair

    assert equivalence(first_contour == second_contour,
                       second_contour == first_contour)


@given(strategies.contours_triplets)
def test_transitivity(contours_triplet: Tuple[Contour, Contour, Contour]
                      ) -> None:
    first_contour, second_contour, third_contour = contours_triplet

    assert implication(first_contour == second_contour
                       and second_contour == third_contour,
                       first_contour == third_contour)


@given(strategies.contours_pairs)
def test_connection_with_inequality(contours_pair: Tuple[Contour, Contour]
                                    ) -> None:
    first_contour, second_contour = contours_pair

    assert equivalence(not first_contour == second_contour,
                       first_contour != second_contour)
