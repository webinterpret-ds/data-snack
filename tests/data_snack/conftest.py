from dataclasses import field, dataclass
from typing import List, Optional, Text
from unittest.mock import MagicMock

import pytest

from data_snack import Snack
from data_snack.connections import Connection
from data_snack.connections.redis import RedisConnection
from data_snack.entities import Entity, EntityRegistry
from data_snack.serializers import DataclassSerializer


@dataclass
class Car(Entity):
    index: Text
    brand: Optional[Text] = field(default=None)

    class Meta:
        keys: List[str] = ["index"]
        excluded_fields: List[str] = []
        version = 1


@pytest.fixture
def serializer() -> DataclassSerializer:
    return DataclassSerializer(Car)


@pytest.fixture
def example_entity() -> Car:
    return Car(index="1", brand="Volkswagen Passat")


@pytest.fixture
def example_entities() -> List[Car]:
    return [
        Car(index="1", brand="Volkswagen Passat"),
        Car(index="2", brand="Volkswagen Golf"),
    ]


@pytest.fixture
def example_entities_with_duplicates() -> List[Car]:
    return [
        Car(index="1", brand="Volkswagen Passat"),
        Car(index="2", brand="Volkswagen Golf"),
        Car(index="1", brand="Volkswagen Passat"),
    ]


@pytest.fixture
def example_entities_none() -> List[Optional[Car]]:
    return [
        Car(index="1", brand="Volkswagen Passat"),
        None
    ]


@pytest.fixture
def example_entity_hash() -> bytes:
    return (
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f"
    )


@pytest.fixture
def example_entities_hashes() -> List[bytes]:
    return [
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f",
        b"x\x9c\x8bV7R\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdSp\xcf\xcfIS\x8f\x05\x00W\xdd\x07\x9c",
    ]


@pytest.fixture
def example_entities_with_duplicates_hashes() -> List[bytes]:
    return [
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f",
        b"x\x9c\x8bV7R\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdSp\xcf\xcfIS\x8f\x05\x00W\xdd\x07\x9c",
        b"x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f",
    ]


@pytest.fixture
def example_entities_hashes_none() -> List[bytes]:
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


@pytest.fixture
def entity_registry():
    return EntityRegistry(entity_type=Car, serializer=DataclassSerializer(Car))
