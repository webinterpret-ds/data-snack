from typing import List

import numpy as np

from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car
import pytest


@pytest.mark.parametrize(
    "entity_instance, entity_hash",
    [
        (Car(index="1", brand="dummy"), b'x\x9c\x8bV7T\xd7QPO)\xcd\xcd\xadT\x8f\x05\x00\x1aq\x03\xfe'),
        (Car(index="1", brand=None), b"x\x9c\x8bV7T\xd7Q\xf0\xcb\xcfK\x8d\x05\x00\x10\x12\x03\x14"),
        # note: serialize converts np.nan to None
        (Car(index="1", brand=np.nan), b"x\x9c\x8bV7T\xd7Q\xf0\xcb\xcfK\x8d\x05\x00\x10\x12\x03\x14"),
    ]
)
def test_serialize(
    serializer: DataclassSerializer, entity_instance: Car, entity_hash: bytes
) -> None:
    """Testing serializing (compressing) a single entity."""
    entity_hash = serializer.serialize(entity=entity_instance)
    assert entity_hash == entity_hash


def test_serialize_many(
    serializer: DataclassSerializer,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
) -> None:
    """Testing serializing a list of multiple entities to a list of hashes."""
    entities_hashes = serializer.serialize(entity=example_entities, many=True)
    assert entities_hashes == example_entities_hashes


def test_deserialize(
    serializer: DataclassSerializer, example_entity: Car, example_entity_hash: bytes
) -> None:
    """Testing deserializing (decompressing) a single entity."""
    entity = serializer.deserialize(data=example_entity_hash)
    assert entity == example_entity


def test_deserialize_many(
    serializer: DataclassSerializer,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes."""
    entities = serializer.deserialize(data=example_entities_hashes, many=True)
    assert entities == example_entities


def test_serialize_many_none(
        serializer: DataclassSerializer,
        example_entities_none: List[Car],
        example_entities_hashes_none: List[bytes],
) -> None:
    """Testing serializing a list of multiple entities to a list of hashes."""
    entities_hashes = serializer.serialize(entity=example_entities_none, many=True)
    assert entities_hashes == example_entities_hashes_none


def test_deserialize_many_none(
        serializer: DataclassSerializer,
        example_entities_none: List[Car],
        example_entities_hashes_none: List[bytes],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes."""
    entities = serializer.deserialize(data=example_entities_hashes_none, many=True)
    assert entities == example_entities_none
