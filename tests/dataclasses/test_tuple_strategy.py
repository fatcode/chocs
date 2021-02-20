from collections import namedtuple
from typing import NamedTuple, Tuple

from chocs.dataclasses import get_strategy_for


def test_hydrate_generic_tuple() -> None:
    # given
    strategy = get_strategy_for(tuple)
    items = ["a", 1, 2.1, True]

    # when
    hydrated_items = strategy.hydrate(items)

    # then
    assert hydrated_items == ("a", 1, 2.1, True)


def test_hydrate_typed_tuple() -> None:
    # given
    strategy = get_strategy_for(Tuple[str, int, str, int])
    items = ["a", 1, 2.1, True]

    # when
    hydrated_items = strategy.hydrate(items)

    # then
    assert hydrated_items == ("a", 1, "2.1", 1)


def test_hydrate_ellipsis_tuple() -> None:
    # given
    strategy = get_strategy_for(Tuple[str, ...])
    items = ["a", 1, 2.1, True]

    # when
    hydrated_items = strategy.hydrate(items)

    # then
    assert hydrated_items == ("a", "1", "2.1", "True")


def test_extract_simple_tuple() -> None:
    # given
    strategy = get_strategy_for(tuple)

    items = ("a", 1, 2.1, True)

    # when
    extracted_items = strategy.extract(items)

    # then
    assert extracted_items == ["a", 1, 2.1, True]


def test_extract_typed_tuple() -> None:
    # given
    strategy = get_strategy_for(Tuple[str, int, str, int])
    items = ("a", 1, 2.1, True)

    # when
    extracted_items = strategy.extract(items)

    # then
    assert extracted_items == ["a", 1, "2.1", 1]


def test_extract_ellipsis_tuple() -> None:
    # given
    strategy = get_strategy_for(Tuple[str, ...])
    items = ("a", 1, 2.1, True)

    # when
    extracted_items = strategy.extract(items)

    # then
    assert extracted_items == ["a", "1", "2.1", "True"]
