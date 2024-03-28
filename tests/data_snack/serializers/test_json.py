from typing import Dict, List, Optional

import pytest

from data_snack.serializers import JsonSerializer
from tests.data_snack.conftest import Car


@pytest.fixture
def serializer() -> JsonSerializer:
    return JsonSerializer(Car)


@pytest.fixture
def example_entities_jsons() -> List[Dict]:
    return [
        {"index": "1", "brand": "Volkswagen Passat"},
        {"index": "2", "brand": "Volkswagen Golf"}
    ]


@pytest.fixture
def example_entities_jsons_none() -> List[Dict]:
    return [
        {"index": "1", "brand": "Volkswagen Passat"},
        None,
    ]


@pytest.fixture
def example_entity_json() -> Dict:
    return {"index": "1", "brand": "Volkswagen Passat"}


@pytest.mark.parametrize(
    "entity_instance, expected_entity_json",
    [
        (
            Car(index="1", brand="dummy"),
            {"index": "1", "brand": "dummy"},
        ),
        (
            Car(index="1", brand=None),
            {"index": "1", "brand": None},
        ),
        # TODO: brand=np.nan is converted to "nan" by Car constructor,
        #  behavior of JsonSerializer is different than DataClassSerializer
        # (
        #     Car(index="1", brand=np.nan),
        #     {"index": "1", "brand": None},
        # ),
    ],
)
def test_serialize(
    serializer: JsonSerializer, entity_instance: Car, expected_entity_json: Dict
) -> None:
    """Testing serializing a single entity."""
    entity_json = serializer.serialize(entity=entity_instance)
    assert entity_json == expected_entity_json


def test_serialize_many(
    serializer: JsonSerializer,
    example_entities: List[Car],
    example_entities_jsons: List[bytes],
) -> None:
    """Testing serializing a list of multiple entities to a list of dicts."""
    entities_hashes = serializer.serialize(entity=example_entities, many=True)
    assert entities_hashes == example_entities_jsons


def test_deserialize(
    serializer: JsonSerializer, example_entity: Car, example_entity_json: Dict
) -> None:
    """Testing deserializing a single entity."""
    entity = serializer.deserialize(data=example_entity_json)
    assert entity == example_entity


def test_deserialize_none(serializer: JsonSerializer, example_entity: Car) -> None:
    """Testing deserializing a None value."""
    entity = serializer.deserialize(data=None)
    assert entity is None


def test_deserialize_many(
    serializer: JsonSerializer,
    example_entities: List[Car],
    example_entities_jsons: List[Dict],
) -> None:
    """Testing deserializing a list of multiple entities from a list of dicts."""
    entities = serializer.deserialize(data=example_entities_jsons, many=True)
    assert entities == example_entities


def test_deserialize_many_with_none(
    serializer: JsonSerializer,
    example_entities_none: List[Car],
    example_entities_jsons_none: List[Optional[Dict]],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes with None values."""
    entities = serializer.deserialize(data=example_entities_jsons_none, many=True)
    assert entities == example_entities_none
