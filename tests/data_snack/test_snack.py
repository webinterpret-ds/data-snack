from typing import List

import pytest

from data_snack import Snack, EntityWrap, DataFrameWrap
from data_snack.entities import EntityRegistry
from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car


@pytest.fixture
def snack_car(snack: Snack) -> Snack:
    snack.register_entity(Car, keys=['index'])
    return snack


def test_register_entity(snack: Snack) -> None:
    snack.register_entity(Car, keys=['index'])
    registry = snack.registry.get('Car')
    assert type(registry) is EntityRegistry
    assert registry.entity_type == Car
    assert type(registry.serializer) is DataclassSerializer
    assert registry.serializer.entity_type is Car
    assert registry.keys == ['index']


def test_create_wrap(snack_car: Snack) -> None:
    wrap = snack_car.create_wrap(Car)
    assert type(wrap) is EntityWrap
    assert wrap.entity_type is Car
    assert wrap.snack == snack_car


def test_create_custom_wrap(snack_car: Snack) -> None:
    wrap = snack_car.create_wrap(Car, DataFrameWrap)
    assert type(wrap) is DataFrameWrap


def test_set(snack_car: Snack, example_entity: Car) -> None:
    snack_car.connection.connection.set.return_value = True

    key = snack_car.set(entity=example_entity)
    assert key == "Car-1"


def test_get(snack_car: Snack, example_entity: Car, example_entity_hash: bytes) -> None:
    snack_car.connection.connection.get.return_value = example_entity_hash
    entity = snack_car.get(Car, ["1"])
    assert entity == example_entity


def test_get_many(snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]) -> None:
    snack_car.connection.connection.mget.return_value = example_entities_hashes
    entities = snack_car.get_many(Car, [["1"], ["2"]])
    assert entities == example_entities


def test_set_many(snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]) -> None:
    expected_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.mset.return_value = expected_keys
    keys = snack_car.set_many(example_entities)
    assert keys == expected_keys

    expected_payload = dict(zip(expected_keys, example_entities_hashes))
    snack_car.connection.connection.mset.assert_called_with(expected_payload)


def test_keys(snack_car: Snack) -> None:
    expected_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.keys.return_value = expected_keys
    keys = snack_car.keys(Car)

    assert keys == expected_keys
