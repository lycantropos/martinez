import pickle

from _martinez import Contour
from hypothesis import given

from . import strategies


@given(strategies.contours)
def test_round_trip(contour: Contour) -> None:
    assert pickle.loads(pickle.dumps(contour)) == contour
