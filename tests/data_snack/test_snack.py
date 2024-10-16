from typing import List, Optional
from unittest.mock import call

import pytest

from data_snack import DataFrameWrap, EntityWrap, Snack
from data_snack.connections import Connection
from data_snack.exceptions import EntityAlreadyRegistered
from data_snack.key_factories.cluster import ClusterKey
from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car, CarOwner, Registration


@pytest.fixture
def snack_registration(snack: Snack) -> Snack:
    snack.register_entity(Car)
    snack.register_entity(CarOwner)
    return snack


@pytest.fixture
def snack_factory_key_cluster(db_connection: Connection) -> Snack:
    snack = Snack(connection=db_connection, key_factory=ClusterKey)
    snack.register_entity(Car)
    snack.register_entity(CarOwner)
    return snack


def test__register_entity(snack: Snack) -> None:
    snack.register_entity(Car)

    serializer = snack.registry.get(Car)
    assert type(serializer) is DataclassSerializer


def test__register_entity_duplicated(snack_registration: Snack) -> None:
    """Testing if exception is risen if Entity duplicated"""
    with pytest.raises(EntityAlreadyRegistered):
        snack_registration.register_entity(Car)


def test__snack_custom_factory_key(
    snack_factory_key_cluster: Snack, example_car_entity: Car, example_car_entity_hash: bytes
) -> None:
    """Testing using custom key_factory_cluster"""
    _snack = snack_factory_key_cluster
    _snack.connection.connection.get.return_value = example_car_entity_hash
    _snack.get(Car, ["1"])
    _snack.connection.connection.get.assert_called_with("{Car-1}-1")


def test__create_wrap(snack_registration: Snack) -> None:
    wrap = snack_registration.create_wrap(Car)
    assert type(wrap) is EntityWrap
    assert wrap.entity_type is Car
    assert wrap.snack == snack_registration


def test__create_custom_wrap(snack_registration: Snack) -> None:
    wrap = snack_registration.create_wrap(Car, DataFrameWrap)
    assert type(wrap) is DataFrameWrap


def test__get(
    snack_registration: Snack, example_car_entity: Car, example_car_entity_hash: bytes
) -> None:
    snack_registration.connection.connection.get.return_value = example_car_entity_hash

    entity = snack_registration.get(Car, ["1"])
    assert entity == example_car_entity
    snack_registration.connection.connection.get.assert_called_with("Car-1-1")


def test__get_compound(
    snack_registration: Snack,
    example_registration_entity: Registration,
    example_car_entity_hash: bytes,
    example_car_owner_entity_hash: bytes,
) -> None:
    snack_registration.connection.connection.get.side_effect = [example_car_entity_hash, example_car_owner_entity_hash]

    entity = snack_registration.get(Registration, ["1", "1"])
    assert entity == example_registration_entity
    snack_registration.connection.connection.get.assert_has_calls([call("Car-1-1"), call("CarOwner-1-1_1")])


def test__get__missing_key(snack_registration: Snack) -> None:
    snack_registration.connection.connection.get.return_value = None

    entity = snack_registration.get(Car, [["1"]])
    assert entity is None


def test__get_compound__missing_optional_source(
    snack_registration: Snack,
    example_registration_entity_no_car_owner: Registration,
    example_car_entity_hash: bytes
) -> None:
    snack_registration.connection.connection.get.side_effect = [example_car_entity_hash, None]

    entity = snack_registration.get(Registration, ["1", "1"])
    assert entity == example_registration_entity_no_car_owner


def test__get_compound__missing_mandatory_source(
    snack_registration: Snack,
    example_car_owner_entity_hash: bytes
) -> None:
    snack_registration.connection.connection.get.side_effect = [None, example_car_owner_entity_hash]

    entity = snack_registration.get(Registration, ["1", "1"])
    assert entity is None


def test__delete(snack_registration: Snack, example_car_entity: Car) -> None:
    snack_registration.connection.connection.delete.return_value = 1

    deleted = snack_registration.delete(Car, ["1"])
    assert deleted


def test__set(snack_registration: Snack, example_car_entity: Car, example_car_entity_hash: bytes) -> None:
    expected_key = "Car-1-1"
    snack_registration.connection.connection.set.return_value = True

    key = snack_registration.set(entity=example_car_entity)
    assert key == expected_key
    snack_registration.connection.connection.set.assert_called_with(expected_key, example_car_entity_hash)


def test__get_many(
    snack_registration: Snack, example_car_entities: List[Car], example_car_entities_hashes: List[bytes]
) -> None:
    snack_registration.connection.connection.mget.return_value = example_car_entities_hashes

    entities = snack_registration.get_many(Car, [["1"], ["2"]])
    assert entities == example_car_entities


def test__get_many_compound(
    snack_registration: Snack,
    example_registration_entities: List[Registration],
    example_car_entities_hashes: List[bytes],
    example_car_owner_entities_hashes: List[bytes],
) -> None:
    snack_registration.connection.connection.mget.side_effect = [
        example_car_entities_hashes,
        example_car_owner_entities_hashes,
    ]

    entities = snack_registration.get_many(Registration, [["1", "1"], ["2", "2"]])
    assert entities == example_registration_entities


def test__get_many_missing_data(
    snack_registration: Snack,
    example_car_entities_none: List[Optional[Car]],
    example_car_entities_hashes_none: List[Optional[bytes]],
) -> None:
    snack_registration.connection.connection.mget.return_value = example_car_entities_hashes_none

    entities = snack_registration.get_many(Car, [["1"], ["2"]])
    assert entities == example_car_entities_none


def test__get_many_compound___missing_mandatory_data(
    snack_registration: Snack,
    example_registration_entities_none: List[Optional[Registration]],
    example_car_entities_hashes_none: List[Optional[bytes]],
    example_car_owner_entities_hashes: List[bytes],
) -> None:
    snack_registration.connection.connection.mget.side_effect = [
        example_car_entities_hashes_none,
        example_car_owner_entities_hashes,
    ]

    entities = snack_registration.get_many(Registration, [["1", "1"], ["2", "2"]])
    assert entities == example_registration_entities_none


def test__get_many_compound___missing_optional_data(
    snack_registration: Snack,
    example_registration_entities_no_car_owner: List[Registration],
    example_car_entities_hashes: List[bytes],
    example_car_owner_entities_hashes_none: List[Optional[bytes]],
) -> None:
    snack_registration.connection.connection.mget.side_effect = [
        example_car_entities_hashes,
        example_car_owner_entities_hashes_none,
    ]

    entities = snack_registration.get_many(Registration, [["1", "1"], ["2", "2"]])
    assert entities == example_registration_entities_no_car_owner


def test__set_many(
    snack_registration: Snack, example_car_entities: List[Car], example_car_entities_hashes: List[bytes]
) -> None:
    expected_keys = ["Car-1-1", "Car-1-2"]
    snack_registration.connection.connection.mset.return_value = expected_keys

    keys = snack_registration.set_many(example_car_entities)
    assert keys == expected_keys
    expected_payload = dict(zip(expected_keys, example_car_entities_hashes))
    snack_registration.connection.connection.mset.assert_called_with(expected_payload)


def test__set_many_empty_list_of_entity_passed_expect_none_returned(snack_registration: Snack) -> None:
    result = snack_registration.set_many(entities=[])
    assert result is None


def test__delete_many(
    snack_registration: Snack, example_car_entities: List[Car], example_car_entities_hashes: List[bytes]
) -> None:
    deleted_keys = ["Car-1-1", "Car-1-2"]
    snack_registration.connection.connection.delete.return_value = 2

    deleted = snack_registration.delete_many(Car, [["1"], ["2"]])
    assert deleted
    snack_registration.connection.connection.delete.assert_called_with(*deleted_keys)


def test__keys(snack_registration: Snack) -> None:
    expected_keys = ["Car-1-1", "Car-1-2"]
    snack_registration.connection.connection.keys.return_value = expected_keys

    keys = snack_registration.keys(Car)
    assert keys == expected_keys
    snack_registration.connection.connection.keys.assert_called_once_with("Car-1-*")
