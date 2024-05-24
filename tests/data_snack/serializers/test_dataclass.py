from typing import List

import numpy as np
import pytest

from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car


@pytest.mark.parametrize(
    "entity_instance, entity_hash",
    [
        (
            Car(index="1", brand="dummy"),
            b"x\x9c\x8bV7T\xd7QPO)\xcd\xcd\xadT\x8f\x05\x00\x1aq\x03\xfe",
        ),
        (
            Car(index="1", brand=None),
            b"x\x9c\x8bV7T\xd7Q\xf0\xcb\xcfK\x8d\x05\x00\x10\x12\x03\x14",
        ),
        # note: serialize converts np.nan to None
        (
            Car(index="1", brand=np.nan),
            b"x\x9c\x8bV7T\xd7Q\xf0\xcb\xcfK\x8d\x05\x00\x10\x12\x03\x14",
        ),
    ],
)
def test_serialize(
    car_serializer: DataclassSerializer, entity_instance: Car, entity_hash: bytes
) -> None:
    """Testing serializing (compressing) a single entity."""
    entity_hash = car_serializer.serialize(entity=entity_instance)
    assert entity_hash == entity_hash


def test_serialize_many(
    car_serializer: DataclassSerializer,
    example_car_entities: List[Car],
    example_car_entities_hashes: List[bytes],
) -> None:
    """Testing serializing a list of multiple entities to a list of hashes."""
    entities_hashes = car_serializer.serialize(entity=example_car_entities, many=True)
    assert entities_hashes == example_car_entities_hashes


def test_deserialize(
    car_serializer: DataclassSerializer, example_car_entity: Car, example_car_entity_hash: bytes
) -> None:
    """Testing deserializing (decompressing) a single entity."""
    entity = car_serializer.deserialize(data=example_car_entity_hash)
    assert entity == example_car_entity


def test_deserialize_none(
    car_serializer: DataclassSerializer, example_car_entity: Car, example_car_entity_hash: bytes
) -> None:
    """Testing deserializing (decompressing) a None value."""
    entity = car_serializer.deserialize(data=None)
    assert entity is None


def test_deserialize_many(
    car_serializer: DataclassSerializer,
    example_car_entities: List[Car],
    example_car_entities_hashes: List[bytes],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes."""
    entities = car_serializer.deserialize(data=example_car_entities_hashes, many=True)
    assert entities == example_car_entities


def test_deserialize_many_with_none(
    car_serializer: DataclassSerializer,
    example_car_entities_none: List[Car],
    example_car_entities_hashes_none: List[bytes],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes with None values."""
    entities = car_serializer.deserialize(data=example_car_entities_hashes_none, many=True)
    assert entities == example_car_entities_none
