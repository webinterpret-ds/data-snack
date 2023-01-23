from typing import List
from unittest.mock import call

import pytest

from data_snack import EntityWrap, Snack
from tests.data_snack.conftest import Car


@pytest.fixture
def wrap_car(snack: Snack) -> EntityWrap:
    snack.register_entity(Car)
    return snack.create_wrap(Car)


def test_entity_type_name(wrap_car: EntityWrap):
    """Testing getting name of wrapped Entity."""
    assert wrap_car.entity_type_name == "Car"


def test_get(wrap_car: EntityWrap, example_entity: Car, example_entity_hash: bytes):
    """Testing getting a single Entity based of the provided key."""
    wrap_car.snack.connection.connection.get.return_value = example_entity_hash

    entity = wrap_car.get(["1"])
    assert entity == example_entity


def test_set(wrap_car: EntityWrap, example_entity: Car, example_entity_hash: bytes):
    """Testing setting a single Entity based for the provided key."""
    expected_key = "Car-1"
    wrap_car.snack.connection.connection.set.return_value = expected_key

    result = wrap_car.set(example_entity, 100)
    assert result == expected_key
    wrap_car.snack.connection.connection.set.assert_called_with(
        expected_key, example_entity_hash, ex=100
    )


def test_delete(wrap_car: EntityWrap, example_entity: Car, example_entity_hash: bytes):
    """Testing deleting a single Entity based of the provided key."""
    wrap_car.snack.connection.connection.delete.return_value = 1

    deleted = wrap_car.delete(["1"])
    assert deleted


def test_get_many(
    wrap_car: EntityWrap,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
):
    """Testing getting multiple Entity objects based of the provided list of keys."""
    wrap_car.snack.connection.connection.mget.return_value = example_entities_hashes

    entities = wrap_car.get_many([["1"], ["2"]])
    assert entities == example_entities


def test_set_many(
    wrap_car: EntityWrap,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
):
    """Testing setting multiple Entity objects based of the provided list of keys."""
    expected_keys = ["Car-1", "Car-2"]
    wrap_car.snack.connection.connection.mset.return_value = expected_keys

    keys = wrap_car.set_many(example_entities)
    assert keys == expected_keys
    expected_payload = dict(zip(expected_keys, example_entities_hashes))
    wrap_car.snack.connection.connection.mset.assert_called_with(expected_payload)


def test_delete_many(
    wrap_car: EntityWrap,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
):
    """Testing deleting multiple Entity objects based of the provided list of keys."""
    deleted_keys = ["Car-1", "Car-2"]
    wrap_car.snack.connection.connection.delete.return_value = 2

    deleted = wrap_car.delete_many([["1"], ["2"]])
    assert deleted
    wrap_car.snack.connection.connection.delete.assert_called_with(*deleted_keys)


def test_keys(wrap_car: EntityWrap):
    expected_keys = ["Car-1", "Car-2"]
    wrap_car.snack.connection.connection.keys.return_value = expected_keys

    keys = wrap_car.keys()
    assert keys == expected_keys
