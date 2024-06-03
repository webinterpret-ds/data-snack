from typing import Dict, List, Optional

import pytest

from data_snack.serializers import JsonSerializer
from tests.data_snack.conftest import Car


@pytest.fixture
def car_serializer() -> JsonSerializer:
    return JsonSerializer(Car)


@pytest.fixture
def example_car_entities_jsons() -> List[Dict]:
    return [
        {"index": "1", "brand": "Volkswagen Passat"},
        {"index": "2", "brand": "Volkswagen Golf"}
    ]


@pytest.fixture
def example_car_entities_jsons_none() -> List[Dict]:
    return [
        {"index": "1", "brand": "Volkswagen Passat"},
        None,
    ]


@pytest.fixture
def example_car_entity_json() -> Dict:
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
    car_serializer: JsonSerializer, entity_instance: Car, expected_entity_json: Dict
) -> None:
    """Testing serializing a single entity."""
    entity_json = car_serializer.serialize(entity=entity_instance)
    assert entity_json == expected_entity_json


def test_serialize_many(
    car_serializer: JsonSerializer,
    example_car_entities: List[Car],
    example_car_entities_jsons: List[bytes],
) -> None:
    """Testing serializing a list of multiple entities to a list of dicts."""
    entities_hashes = car_serializer.serialize(entity=example_car_entities, many=True)
    assert entities_hashes == example_car_entities_jsons


def test_deserialize(
    car_serializer: JsonSerializer, example_car_entity: Car, example_car_entity_json: Dict
) -> None:
    """Testing deserializing a single entity."""
    entity = car_serializer.deserialize(data=example_car_entity_json)
    assert entity == example_car_entity


def test_deserialize_none(car_serializer: JsonSerializer, example_car_entity: Car) -> None:
    """Testing deserializing a None value."""
    entity = car_serializer.deserialize(data=None)
    assert entity is None


def test_deserialize_many(
    car_serializer: JsonSerializer,
    example_car_entities: List[Car],
    example_car_entities_jsons: List[Dict],
) -> None:
    """Testing deserializing a list of multiple entities from a list of dicts."""
    entities = car_serializer.deserialize(data=example_car_entities_jsons, many=True)
    assert entities == example_car_entities


def test_deserialize_many_with_none(
    car_serializer: JsonSerializer,
    example_car_entities_none: List[Car],
    example_car_entities_jsons_none: List[Optional[Dict]],
) -> None:
    """Testing deserializing a list of multiple entities from a list of hashes with None values."""
    entities = car_serializer.deserialize(data=example_car_entities_jsons_none, many=True)
    assert entities == example_car_entities_none
