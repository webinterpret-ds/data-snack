from typing import List

from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car
import pytest


def test_serialize(
    serializer: DataclassSerializer, example_entity: Car, example_entity_hash: bytes
) -> None:
    """Testing serializing (compressing) a single entity."""
    entity_hash = serializer.serialize(entity=example_entity)
    assert entity_hash == example_entity_hash


def test_serialize_multi(
    serializer: DataclassSerializer,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
) -> None:
    """Testing serializing a list of multiple entities to a list of hashes."""
    entities_hashes = serializer.serialize(entity=example_entities, many=True)
    assert entities_hashes == example_entities_hashes


@pytest.mark.parametrize(
    "entity_instance, entity_hash",
    [
        (Car(index="1", brand="dummy"), b'x\x9c\x8bV7T\xd7QPO)\xcd\xcd\xadT\x8f\x05\x00\x1aq\x03\xfe'),
        (Car(index="1", brand=None), b"x\x9c\x8bV7T\xd7Q\xf0\xcb\xcfK\x8d\x05\x00\x10\x12\x03\x14"),
        # note: the hash below is for brand=np.nan
        (Car(index="1", brand=None), b"x\x9c\x8bV7T\xd7QP\xcfK\xccS\x8f\x05\x00\x12\x0f\x03\x0f"),
    ]
)
def test_deserialize(
    serializer: DataclassSerializer, entity_instance: Car, entity_hash: bytes
) -> None:
    """Testing deserializing (decompressing) a single entity."""
    entity = serializer.deserialize(data=entity_hash)
    assert entity == entity_instance


def test_deserialize_multi(
    serializer: DataclassSerializer,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes."""
    entities = serializer.deserialize(data=example_entities_hashes, many=True)
    assert entities == example_entities
