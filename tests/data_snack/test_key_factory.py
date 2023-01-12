from typing import List, Text

import pytest

from data_snack.key_factory import key_factory, key_factory_cluster


@pytest.mark.parametrize(
    "entity_name,key_values,expected_key",
    [
        ("Entity", ["A"], "Entity-A"),
        ("Entity", ["A", "B"], "Entity-A_B"),
        ("Entity", [1], "Entity-1"),
        ("Entity", [1, 2], "Entity-1_2"),
    ],
)
def test_key_factory(
    entity_name: Text, key_values: List[Text], expected_key: Text
) -> None:
    key = key_factory(entity_name, *key_values)
    assert key == expected_key


@pytest.mark.parametrize(
    "entity_name,key_values,expected_key",
    [
        ("Entity", ["A"], "{Entity}-A"),
        ("Entity", ["A", "B"], "{Entity}-A_B"),
        ("Entity", [1], "{Entity}-1"),
        ("Entity", [1, 2], "{Entity}-1_2"),
    ],
)
def test_key_factory_cluster(
    entity_name: Text, key_values: List[Text], expected_key: Text
) -> None:
    key = key_factory_cluster(entity_name, *key_values)
    assert key == expected_key
