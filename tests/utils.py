import math
import pickle
from functools import partial
from itertools import repeat
from types import MappingProxyType
from typing import (Any,
                    Callable,
                    Dict,
                    Hashable,
                    Iterable,
                    List,
                    Optional,
                    Sequence,
                    Tuple,
                    TypeVar)

from hypothesis import strategies
from hypothesis.strategies import SearchStrategy

from martinez.hints import Scalar
from tests.port_tests.utils import PortedSweepEvent

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy
AnyBoundingBox = TypeVar('AnyBoundingBox')
AnySweepEvent = TypeVar('AnySweepEvent')

MAX_VALUE = 10 ** 4
MIN_VALUE = -MAX_VALUE
MAX_CONTOURS_COUNT = 5
MAX_NESTING_DEPTH = 3


def identity(value: Domain) -> Domain:
    return value


def _cleavage(functions: Iterable[Callable[[Domain], Range]],
              *args: Domain, **kwargs: Domain) -> Iterable[Range]:
    return (function(*args, **kwargs) for function in functions)


def cleave(*functions: Callable[..., Range]) -> Callable[..., Iterable[Range]]:
    return partial(_cleavage, functions)


def _composition(functions: Tuple[Callable[[Domain], Range], ...],
                 *args: Domain, **kwargs: Domain) -> Range:
    result = functions[-1](*args, **kwargs)
    for function in reversed(functions[:-1]):
        result = function(result)
    return result


def compose(last_function: Callable[[Domain], Range],
            *functions: Callable[..., Domain]) -> Callable[..., Range]:
    return partial(_composition, (last_function,) + functions)


def cleave_in_tuples(*functions: Callable[[Strategy[Domain]], Strategy[Range]]
                     ) -> Callable[[Strategy[Domain]],
                                   Strategy[Tuple[Range, ...]]]:
    return compose(pack(strategies.tuples), cleave(*functions))


def pack(function: Callable[..., Range]
         ) -> Callable[[Iterable[Domain]], Range]:
    return partial(apply, function)


def apply(function: Callable[..., Range],
          args: Iterable[Domain],
          kwargs: Dict[str, Any] = MappingProxyType({})) -> Range:
    return function(*args, **kwargs)


to_builder = partial(partial, strategies.builds)


def to_maybe(strategy: Strategy[Domain]) -> Strategy[Optional[Domain]]:
    return strategies.none() | strategy


def to_tuples(elements: Strategy[Domain],
              *,
              size: int) -> Strategy[Tuple[Domain, ...]]:
    return strategies.tuples(*repeat(elements,
                                     times=size))


to_pairs = partial(to_tuples,
                   size=2)
to_triplets = partial(to_tuples,
                      size=3)


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def transpose(sequence: Sequence[Tuple[Domain, ...]]
              ) -> Tuple[Sequence[Domain], ...]:
    sequence_type = type(sequence)
    if not sequence:
        return sequence_type(), sequence_type()
    return tuple(map(sequence_type, zip(*sequence)))


def capacity(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)


def all_unique(iterable: Iterable[Hashable]) -> bool:
    seen = set()
    for element in iterable:
        if element not in seen:
            seen.add(element)
        else:
            return False
    return True


def permute(sequence: Sequence[Domain],
            permutation: Sequence[int]) -> Iterable[Domain]:
    return map(sequence.__getitem__, permutation)


def is_even_permutation(permutation: Sequence[int]) -> bool:
    counter = 0
    for index in range(len(permutation)):
        for next_index in range(index + 1, len(permutation)):
            if permutation[index] > permutation[next_index]:
                counter += 1
    return not counter % 2


def to_valid_coordinates_pairs(candidates: List[Scalar],
                               *,
                               lower_bound: int = 1,
                               upper_bound: int = int(math.sqrt(MAX_VALUE
                                                                - MIN_VALUE))
                               ) -> Tuple[Scalar, Scalar]:
    start, *rest, end = candidates
    if not (lower_bound <= end - start <= upper_bound):
        start = next((candidate
                      for candidate in rest
                      if lower_bound <= end - candidate <= upper_bound),
                     end - (upper_bound - lower_bound))
    return start, end


def pickle_round_trip(object_: Domain) -> Domain:
    return pickle.loads(pickle.dumps(object_))


def is_sweep_event_non_degenerate(event: AnySweepEvent) -> bool:
    return not event.segment.is_degenerate


def to_double_nested_sweep_event(event: AnySweepEvent) -> AnySweepEvent:
    if event.other_event is None:
        event.other_event = event
    elif event.other_event.other_event is None:
        event.other_event.other_event = event
    return event


def are_sweep_events_pair_with_different_polygon_types(
        events_pair: Tuple[AnySweepEvent, AnySweepEvent]) -> bool:
    first_event, second_event = events_pair
    return first_event.polygon_type != second_event.polygon_type


def to_bounding_boxes_offset(first_bounding_box: AnyBoundingBox,
                             second_bounding_box: AnyBoundingBox
                             ) -> Tuple[Scalar, Scalar]:
    delta_x = (max(first_bounding_box.x_max, second_bounding_box.x_max)
               - min(first_bounding_box.x_min, second_bounding_box.x_min))
    delta_y = (max(first_bounding_box.y_max, second_bounding_box.y_max)
               - min(first_bounding_box.y_min, second_bounding_box.y_min))
    return delta_x, delta_y


traverse_sweep_event = PortedSweepEvent._traverse


def make_cyclic(sweep_events: Strategy[AnySweepEvent]
                ) -> Strategy[AnySweepEvent]:
    def to_cyclic_sweep_events(event: AnySweepEvent
                               ) -> Strategy[AnySweepEvent]:
        events = traverse_sweep_event(event, {}, {})
        links = to_links(len(events))
        return (strategies.builds(to_left_relinked_sweep_event,
                                  strategies.just(events), links)
                | strategies.builds(to_right_relinked_sweep_event,
                                    strategies.just(events), links))

    return sweep_events.flatmap(to_cyclic_sweep_events)


def to_double_nested_sweep_events(strategy: Strategy[AnySweepEvent]
                                  ) -> Strategy[AnySweepEvent]:
    return strategy.map(to_double_nested_sweep_event)


def to_links(events_count: int) -> Strategy[Dict[int, int]]:
    return strategies.dictionaries(strategies.integers(0, events_count - 1),
                                   strategies.integers(0, events_count - 1),
                                   min_size=events_count // 2)


def to_left_relinked_sweep_event(events: List[AnySweepEvent],
                                 links: Dict[int, int]) -> AnySweepEvent:
    for source, destination in links.items():
        events[source].other_event = events[destination]
    return events[0]


def to_right_relinked_sweep_event(events: List[AnySweepEvent],
                                  links: Dict[int, int]) -> AnySweepEvent:
    for source, destination in links.items():
        events[source].prev_in_result_event = events[destination]
    return events[0]
