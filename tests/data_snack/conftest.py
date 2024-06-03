from dataclasses import field, dataclass
from typing import List, Optional
from unittest.mock import MagicMock

import pytest

from data_snack import Snack
from data_snack.connections import Connection
from data_snack.connections.redis import RedisConnection
from data_snack.entities import Entity, CompoundEntity
from data_snack.entities.models import SourceEntity, EntityFieldMapping
from data_snack.serializers import DataclassSerializer


@dataclass
class Car(Entity):
    index: str
    brand: Optional[str] = field(default=None)

    class Meta:
        keys: List[str] = ["index"]
        excluded_fields: List[str] = []
        version = 1


@dataclass
class Person(Entity):
    index: str
    name: Optional[str] = field(default=None)

    class Meta:
        keys: List[str] = ["index"]
        excluded_fields: List[str] = []
        version = 1


@dataclass
class Registration(CompoundEntity):
    car_index: str
    person_index: str
    brand: Optional[str]
    name: Optional[str]

    class Meta:
        sources: List[SourceEntity] = [
            SourceEntity(
                entity=Car,
                entity_fields_mapping=[
                    EntityFieldMapping(field="car_index", source_field="index"),
                    EntityFieldMapping(field="brand", source_field="brand")
                ]
            ),
            SourceEntity(
                entity=Person,
                entity_fields_mapping=[
                    EntityFieldMapping(field="person_index", source_field="index"),
                    EntityFieldMapping(field="name", source_field="name")
                ]
            )
        ]


@pytest.fixture
def car_serializer() -> DataclassSerializer:
    return DataclassSerializer(Car)


@pytest.fixture
def example_car_entity() -> Car:
    return Car(index="1", brand="Volkswagen Passat")


@pytest.fixture
def example_person_entity() -> Person:
    return Person(index="1", name="Michael Brown")


@pytest.fixture
def example_registration_entity() -> Registration:
    return Registration(car_index="1", person_index="1", brand="Volkswagen Passat", name="Michael Brown")


@pytest.fixture
def example_car_entities() -> List[Car]:
    return [
        Car(index="1", brand="Volkswagen Passat"),
        Car(index="2", brand="Volkswagen Golf"),
    ]


@pytest.fixture
def example_person_entities() -> List[Person]:
    return [
        Person(index="1", name="Michael Brown"),
        Person(index="2", name="John Smith"),
    ]


@pytest.fixture
def example_registration_entities() -> List[Registration]:
    return [
        Registration(car_index="1", person_index="1", brand="Volkswagen Passat", name="Michael Brown"),
        Registration(car_index="2", person_index="2", brand="Volkswagen Golf", name="John Smith"),
    ]


@pytest.fixture
def example_car_entities_with_duplicates() -> List[Car]:
    return [
        Car(index="1", brand="Volkswagen Passat"),
        Car(index="2", brand="Volkswagen Golf"),
        Car(index="1", brand="Volkswagen Passat"),
    ]


@pytest.fixture
def example_car_entities_none() -> List[Optional[Car]]:
    return [
        Car(index="1", brand="Volkswagen Passat"),
        None
    ]


@pytest.fixture
def example_registration_entities_none() -> List[Optional[Registration]]:
    return [
        Registration(car_index="1", person_index="1", brand="Volkswagen Passat", name="Michael Brown"),
        None,
    ]


@pytest.fixture
def example_car_entity_hash() -> bytes:
    return (
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f"
    )


@pytest.fixture
def example_person_entity_hash() -> bytes:
    return (
        b"x\x9c\x8bV7T\xd7QP\xf7\xcdL\xceHL\xcdQp*\xca/\xcfS\x8f\x05\x00E\x03\x06\xad"
    )


@pytest.fixture
def example_car_entities_hashes() -> List[bytes]:
    return [
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f",
        b"x\x9c\x8bV7R\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdSp\xcf\xcfIS\x8f\x05\x00W\xdd\x07\x9c",
    ]


@pytest.fixture
def example_person_entities_hashes() -> List[bytes]:
    return [
        b"x\x9c\x8bV7T\xd7QP\xf7\xcdL\xceHL\xcdQp*\xca/\xcfS\x8f\x05\x00E\x03\x06\xad",
        b"x\x9c\x8bV7R\xd7QP\xf7\xca\xcf\xc8S\x08\xce\xcd,\xc9P\x8f\x05\x001a\x05\x87",
    ]


@pytest.fixture
def example_car_entities_with_duplicates_hashes() -> List[bytes]:
    return [
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f",
        b"x\x9c\x8bV7R\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdSp\xcf\xcfIS\x8f\x05\x00W\xdd\x07\x9c",
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f",
    ]


@pytest.fixture
def example_car_entities_hashes_none() -> List[bytes]:
    return [
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f",
        None,
    ]


@pytest.fixture
def db_connection() -> RedisConnection:
    return RedisConnection(connection=MagicMock())


@pytest.fixture
def snack(db_connection: Connection) -> Snack:
    return Snack(connection=db_connection)
