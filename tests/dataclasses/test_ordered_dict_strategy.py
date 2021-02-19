from chocs.dataclasses import get_strategy_for
from collections import OrderedDict
from typing import OrderedDict as TypingOrderedDict


def test_hydrate_generic_collection_ordered_dict() -> None:
    # given
    strategy = get_strategy_for(OrderedDict)
    input_data = {"int": 1, "float": 2.2, "bool": True, "string": "Hello"}

    # when
    result = strategy.hydrate(input_data)

    # then
    assert isinstance(result, OrderedDict)
    assert result == OrderedDict({"int": 1, "float": 2.2, "bool": True, "string": "Hello"})


def test_hydrate_annotated_ordered_dict() -> None:
    # given
    strategy = get_strategy_for(TypingOrderedDict[str, str])
    input_data = {"int": 1, "float": 2.2, "bool": True, "string": "Hello"}

    # when
    result = strategy.hydrate(input_data)

    # then
    assert isinstance(result, OrderedDict)
    assert result == {"int": "1", "float": "2.2", "bool": "True", "string": "Hello"}


def test_extract_generic_collection_ordered_dict() -> None:
    # given
    strategy = get_strategy_for(OrderedDict)
    input_data = OrderedDict({"int": 1, "float": 2.2, "bool": True, "string": "Hello"})

    # when
    result = strategy.extract(input_data)

    # then
    assert not isinstance(result, OrderedDict)
    assert result == {"int": 1, "float": 2.2, "bool": True, "string": "Hello"}


def test_extract_annotated_ordered_dict() -> None:
    # given
    strategy = get_strategy_for(TypingOrderedDict[str, str])
    input_data = OrderedDict({"int": 1, "float": 2.2, "bool": True, "string": "Hello"})

    # when
    result = strategy.extract(input_data)

    # then
    assert not isinstance(result, OrderedDict)
    assert result == {"int": "1", "float": "2.2", "bool": "True", "string": "Hello"}

