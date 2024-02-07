from typing import List, Optional

import pytest

from data_snack import DataFrameWrap, EntityWrap, Snack
from data_snack.connections import Connection
from data_snack.entities import EntityRegistry
from data_snack.exceptions import EntityAlreadyRegistered
from data_snack.key_factories.cluster import ClusterKey
from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car


@pytest.fixture
def snack_car(snack: Snack) -> Snack:
    snack.register_entity(Car)
    return snack


@pytest.fixture
def snack_factory_key_cluster(db_connection: Connection) -> Snack:
    snack = Snack(connection=db_connection, key_factory=ClusterKey)
    snack.register_entity(Car)
    return snack


def test__register_entity(snack: Snack) -> None:
    snack.register_entity(Car)

    serializer = snack.registry.get(Car)
    assert type(serializer) is DataclassSerializer


def test__register_entity_duplicated(snack_car: Snack) -> None:
    """Testing if exception is risen if Entity duplicated"""
    with pytest.raises(EntityAlreadyRegistered):
        snack_car.register_entity(Car)


def test__snack_custom_factory_key(
    snack_factory_key_cluster: Snack, example_entity: Car, example_entity_hash: bytes
) -> None:
    """Testing using custom key_factory_cluster"""
    _snack = snack_factory_key_cluster
    _snack.connection.connection.get.return_value = example_entity_hash
    _snack.get(Car, ["1"])
    _snack.connection.connection.get.assert_called_with("{Car}-1")


def test__create_wrap(snack_car: Snack) -> None:
    wrap = snack_car.create_wrap(Car)
    assert type(wrap) is EntityWrap
    assert wrap.entity_type is Car
    assert wrap.snack == snack_car


def test__create_custom_wrap(snack_car: Snack) -> None:
    wrap = snack_car.create_wrap(Car, DataFrameWrap)
    assert type(wrap) is DataFrameWrap


def test__get(
    snack_car: Snack, example_entity: Car, example_entity_hash: bytes
) -> None:
    snack_car.connection.connection.get.return_value = example_entity_hash

    entity = snack_car.get(Car, ["1"])
    assert entity == example_entity
    snack_car.connection.connection.get.assert_called_with("Car-1")


def test__get__missing_key(snack_car: Snack, example_entity: Car) -> None:
    snack_car.connection.connection.get.return_value = None

    entity = snack_car.get(Car, [["1"]])
    assert entity is None


def test__delete(snack_car: Snack, example_entity: Car) -> None:
    snack_car.connection.connection.delete.return_value = 1

    deleted = snack_car.delete(Car, ["1"])
    assert deleted


def test__set(
    snack_car: Snack, example_entity: Car, example_entity_hash: bytes
) -> None:
    expected_key = "Car-1"
    snack_car.connection.connection.set.return_value = True

    key = snack_car.set(entity=example_entity)
    assert key == expected_key
    snack_car.connection.connection.set.assert_called_with(
        expected_key, example_entity_hash
    )


def test__get_many(
    snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]
) -> None:
    snack_car.connection.connection.mget.return_value = example_entities_hashes

    entities = snack_car.get_many(Car, [["1"], ["2"]])
    assert entities == example_entities


def test__get_many__missing_data(
    snack_car: Snack,
    example_entities_none: List[Optional[Car]],
    example_entities_hashes_none: List[Optional[bytes]],
) -> None:
    snack_car.connection.connection.mget.return_value = example_entities_hashes_none

    entities = snack_car.get_many(Car, [["1"], ["2"]])
    assert entities == example_entities_none


def test__set_many(
    snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]
) -> None:
    expected_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.mset.return_value = expected_keys

    keys = snack_car.set_many(example_entities)
    assert keys == expected_keys
    expected_payload = dict(zip(expected_keys, example_entities_hashes))
    snack_car.connection.connection.mset.assert_called_with(expected_payload)


def test__set_many_empty_list_of_entity_passed_expect_none_returned(snack_car: Snack) -> None:
    result = snack_car.set_many(entities=[])
    assert result is None


def test__delete_many(
    snack_car: Snack, example_entities: List[Car], example_entities_hashes: List[bytes]
) -> None:
    deleted_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.delete.return_value = 2

    deleted = snack_car.delete_many(Car, [["1"], ["2"]])
    assert deleted
    snack_car.connection.connection.delete.assert_called_with(*deleted_keys)


def test__keys(snack_car: Snack) -> None:
    expected_keys = ["Car-1", "Car-2"]
    snack_car.connection.connection.keys.return_value = expected_keys

    keys = snack_car.keys(Car)
    assert keys == expected_keys
    snack_car.connection.connection.keys.assert_called_once_with("Car-*")
