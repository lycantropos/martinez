import pickle

from hypothesis import given

from martinez.contour import Contour
from . import strategies


@given(strategies.contours)
def test_round_trip(contour: Contour) -> None:
    assert pickle.loads(pickle.dumps(contour)) == contour
