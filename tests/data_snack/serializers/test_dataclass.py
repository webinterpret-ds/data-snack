from typing import List

from data_snack.serializers import DataclassSerializer
from tests.data_snack.conftest import Car


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


def test_deserialize(
    serializer: DataclassSerializer, example_entity: Car, example_entity_hash: bytes
) -> None:
    """Testing deserializing (decompressing) a single entity."""
    entity = serializer.deserialize(data=example_entity_hash)
    assert entity == example_entity


def test_deserialize_multi(
    serializer: DataclassSerializer,
    example_entities: List[Car],
    example_entities_hashes: List[bytes],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes."""
    entities = serializer.deserialize(data=example_entities_hashes, many=True)
    assert entities == example_entities
