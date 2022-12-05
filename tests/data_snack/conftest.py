from typing import Text, List
from unittest.mock import MagicMock

import pytest
from pydantic.dataclasses import dataclass

from data_snack import Snack
from data_snack.connections import Connection
from data_snack.connections.redis import RedisConnection
from data_snack.entities import EntityRegistry, Entity
from data_snack.serializers import DataclassSerializer


@dataclass
class Car(Entity):
    index: Text
    brand: Text


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
def example_entity_hash() -> bytes:
    return b'x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f'


@pytest.fixture
def example_entities_hashes() -> List[bytes]:
    return [
        b'x\x9c\x8bV7T\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdS\x08H,.N,Q\x8f\x05\x00i&\x08\x7f',
        b'x\x9c\x8bV7R\xd7QP\x0f\xcb\xcf\xc9..OLO\xcdSp\xcf\xcfIS\x8f\x05\x00W\xdd\x07\x9c'
    ]


@pytest.fixture
def db_connection() -> RedisConnection:
    return RedisConnection(connection=MagicMock())


@pytest.fixture
def snack(db_connection: Connection) -> Snack:
    return Snack(connection=db_connection)


@pytest.fixture
def entity_registry():
    return EntityRegistry(
        entity_type=Car,
        serializer=DataclassSerializer(Car),
        key_fields=["index"]
    )
