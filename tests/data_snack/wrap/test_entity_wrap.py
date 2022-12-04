from typing import List

import pytest

from data_snack import Snack, EntityWrap
from tests.data_snack.conftest import Car


@pytest.fixture
def wrap_car(snack: Snack) -> EntityWrap:
    snack.register_entity(Car, keys=['index'])
    return snack.create_wrap(Car)


def test_entity_type_name(wrap_car: EntityWrap):
    assert wrap_car.entity_type_name == 'Car'


def test_get(wrap_car: EntityWrap, example_entity: Car, example_entity_hash: bytes):
    wrap_car.snack.connection.connection.get.return_value = example_entity_hash
    entity = wrap_car.get(["1"])
    assert entity == example_entity


def test_get_many(wrap_car: EntityWrap, example_entities: List[Car], example_entities_hashes: List[bytes]):
    wrap_car.snack.connection.connection.mget.return_value = example_entities_hashes
    entities = wrap_car.get_many([["1"], ["2"]])
    assert entities == example_entities


def test_set_many(wrap_car: EntityWrap, example_entities: List[Car], example_entities_hashes: List[bytes]):
    expected_keys = ["Car-1", "Car-2"]
    wrap_car.snack.connection.connection.mset.return_value = expected_keys
    keys = wrap_car.set_many(example_entities)
    assert keys == expected_keys

    expected_payload = dict(zip(expected_keys, example_entities_hashes))
    wrap_car.snack.connection.connection.mset.assert_called_with(expected_payload)


def test_keys(wrap_car: EntityWrap):
    expected_keys = ["Car-1", "Car-2"]
    wrap_car.snack.connection.connection.keys.return_value = expected_keys
    keys = wrap_car.keys()
    assert keys == expected_keys
