from typing import List
from unittest.mock import call

import pytest

from data_snack import Snack, EntityWrap, DataFrameWrap
from data_snack.entities import EntityRegistry
from data_snack.exceptions import EntityAlreadyRegistered
from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car


@pytest.fixture
def snack_car(snack: Snack) -> Snack:
    snack.register_entity(Car, key_fields=['index'])
    return snack


def test_register_entity(snack: Snack) -> None:
    snack.register_entity(Car, key_fields=['index'])

    registry = snack.registry.get('Car')
    assert type(registry) is EntityRegistry
    assert registry.entity_type == Car
    assert type(registry.serializer) is DataclassSerializer
    assert registry.serializer.entity_type is Car
    assert registry.key_fields == ['index']


def test_register_entity_duplicated(snack_car: Snack) -> None:
    """Testing if exception is risen if Entity duplicated"""
    with pytest.raises(EntityAlreadyRegistered):
        snack_car.register_entity(Car, key_fields=['index'])


def test_create_wrap(snack_car: Snack) -> None:
    wrap = snack_car.create_wrap(Car)
    assert type(wrap) is EntityWrap
    assert wrap.entity_type is Car
    assert wrap.snack == snack_car


def test_create_custom_wrap(snack_car: Snack) -> None:
    wrap = snack_car.create_wrap(Car, DataFrameWrap)
    assert type(wrap) is DataFrameWrap


def test_get(snack_car: Snack, example_entity: Car, example_entity_hash: bytes) -> None:
    snack_car.connection.connection.get.return_value = example_entity_hash

    entity = snack_car.get(Car, ["1"])
    assert entity == example_entity


def test_delete(snack_car: Snack, example_entity: Car) -> None:
    snack_car.connection.connection.delete.return_value = 1

    deleted = snack_car.delete(Car, ["1"])
    assert deleted


def test_set(snack_car: Snack, example_entity: Car, example_entity_hash: bytes) -> None:
    expected_key = "Car-1"
    snack_car.connection.connection.set.return_value = True

    key = snack_car.set(entity=example_entity, expire=100)
    assert key == expected_key
    snack_car.connection.connection.set.assert_called_with(
        expected_key,
        example_entity_hash,
        ex=100
    )


def test_get_many(snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]) -> None:
    snack_car.connection.connection.mget.return_value = example_entities_hashes

    entities = snack_car.get_many(Car, [["1"], ["2"]])
    assert entities == example_entities


def test_set_many(snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]) -> None:
    expected_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.set.side_effect = expected_keys

    keys = snack_car.set_many(example_entities, 100)
    assert keys == expected_keys
    expected_payload = dict(zip(expected_keys, example_entities_hashes))
    snack_car.connection.connection.set.assert_has_calls([call(k, v, ex=100) for k, v in expected_payload.items()])


def test_delete_many(snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]) -> None:
    deleted_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.delete.return_value = 2

    deleted = snack_car.delete_many(Car, [["1"], ["2"]])
    assert deleted
    snack_car.connection.connection.delete.assert_called_with(*deleted_keys)


def test_keys(snack_car: Snack) -> None:
    expected_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.keys.return_value = expected_keys

    keys = snack_car.keys(Car)
    assert keys == expected_keys
