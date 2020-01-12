import sys
from decimal import Decimal
from fractions import Fraction
from functools import partial
from typing import (Optional,
                    SupportsFloat)

from _martinez import (EdgeType as BoundEdgeType,
                       OperationType as BoundOperationType,
                       PolygonType as BoundPolygonType)
from hypothesis import strategies

from martinez.boolean import (EdgeType as PortedEdgeType,
                              OperationType as PortedOperationType,
                              PolygonType as PortedPolygonType)
from martinez.hints import Scalar
from tests.utils import (MAX_VALUE,
                         MIN_VALUE,
                         Strategy)

MAX_DIGITS_COUNT = sys.float_info.dig

booleans = strategies.booleans()


def to_decimals(*,
                min_value: Optional[Scalar] = MIN_VALUE,
                max_value: Optional[Scalar] = MAX_VALUE,
                allow_nan: bool = False,
                allow_infinity: bool = False,
                max_digits_count: int = MAX_DIGITS_COUNT) -> Strategy[Decimal]:
    return (strategies.decimals(min_value=min_value,
                                max_value=max_value,
                                allow_nan=allow_nan,
                                allow_infinity=allow_infinity)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_floats(*,
              min_value: Optional[Scalar] = MIN_VALUE,
              max_value: Optional[Scalar] = MAX_VALUE,
              allow_nan: bool = False,
              allow_infinity: bool = False,
              max_digits_count: int = MAX_DIGITS_COUNT) -> Strategy[float]:
    return (strategies.floats(min_value=min_value,
                              max_value=max_value,
                              allow_nan=allow_nan,
                              allow_infinity=allow_infinity)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_fractions(*,
                 min_value: Optional[Scalar] = MIN_VALUE,
                 max_value: Optional[Scalar] = MAX_VALUE,
                 max_denominator: Optional[Scalar] = None,
                 max_digits_count: int = MAX_DIGITS_COUNT
                 ) -> Strategy[Fraction]:
    return (strategies.fractions(min_value=min_value,
                                 max_value=max_value,
                                 max_denominator=max_denominator)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_integers(*,
                min_value: Optional[Scalar] = MIN_VALUE,
                max_value: Optional[Scalar] = MAX_VALUE,
                max_digits_count: int = MAX_DIGITS_COUNT) -> Strategy[int]:
    return (strategies.integers(min_value=min_value,
                                max_value=max_value)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_digits_count(number: Scalar,
                    *,
                    max_digits_count: int = MAX_DIGITS_COUNT) -> Scalar:
    decimal = to_decimal(number).normalize()
    _, significant_digits, exponent = decimal.as_tuple()
    significant_digits_count = len(significant_digits)
    if exponent < 0:
        fixed_digits_count = (1 - exponent
                              if exponent <= -significant_digits_count
                              else significant_digits_count)
    else:
        fixed_digits_count = exponent + significant_digits_count
    if fixed_digits_count <= max_digits_count:
        return number
    whole_digits_count = max(significant_digits_count + exponent, 0)
    if whole_digits_count:
        whole_digits_offset = max(whole_digits_count - max_digits_count, 0)
        decimal /= 10 ** whole_digits_offset
        whole_digits_count -= whole_digits_offset
    else:
        decimal *= 10 ** (-exponent - significant_digits_count)
        whole_digits_count = 1
    decimal = round(decimal, max(max_digits_count - whole_digits_count, 0))
    return type(number)(str(decimal))


def to_decimal(number: SupportsFloat) -> Decimal:
    if isinstance(number, Decimal):
        return number
    elif not isinstance(number, (int, float)):
        number = float(number)
    return Decimal(number)


scalars_strategies_factories = {Decimal: to_decimals,
                                float: to_floats,
                                Fraction: to_fractions,
                                int: to_integers}
scalars_strategies = strategies.sampled_from(
        [factory() for factory in scalars_strategies_factories.values()])
floats = to_floats()
single_precision_floats = to_floats(max_digits_count=MAX_DIGITS_COUNT // 2)
single_precision_scalars_strategies = strategies.sampled_from(
        [factory(max_digits_count=MAX_DIGITS_COUNT // 2)
         if type_ is float or type_ is Decimal
         else factory()
         for type_, factory in scalars_strategies_factories.items()])
unsigned_integers = strategies.integers(0, 65535)
unsigned_integers_lists = strategies.lists(unsigned_integers)
non_negative_integers = strategies.integers(0)
non_negative_integers_lists = strategies.lists(non_negative_integers)
bound_edges_types = strategies.sampled_from(list(BoundEdgeType
                                                 .__members__.values()))
bound_polygons_types = strategies.sampled_from(list(BoundPolygonType
                                                    .__members__.values()))
bound_operations_types = strategies.sampled_from(
        list(BoundOperationType.__members__.values()))
ported_edges_types = strategies.sampled_from(list(PortedEdgeType
                                                  .__members__.values()))
ported_polygons_types = strategies.sampled_from(list(PortedPolygonType
                                                     .__members__.values()))
ported_operations_types = strategies.sampled_from(
        list(PortedOperationType.__members__.values()))
bound_with_ported_edges_types_pairs = strategies.sampled_from(
        [(BoundEdgeType.__members__[name],
          PortedEdgeType.__members__[name])
         for name in (BoundEdgeType.__members__.keys() &
                      PortedEdgeType.__members__.keys())])
bound_with_ported_polygons_types_pairs = strategies.sampled_from(
        [(BoundPolygonType.__members__[name],
          PortedPolygonType.__members__[name])
         for name in (BoundPolygonType.__members__.keys() &
                      PortedPolygonType.__members__.keys())])
bound_with_ported_operations_types_pairs = strategies.sampled_from(
        [(BoundOperationType.__members__[name],
          PortedOperationType.__members__[name])
         for name in (BoundOperationType.__members__.keys() &
                      PortedOperationType.__members__.keys())])
