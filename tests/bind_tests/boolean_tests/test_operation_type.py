from tests.bind_tests.hints import BoundOperationType

from tests.utils import all_unique


def test_basic():
    assert all_unique(BoundOperationType.__members__.values())
