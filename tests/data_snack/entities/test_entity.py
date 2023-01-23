from dataclasses import dataclass
from typing import Type, List

import pytest

from data_snack.entities import Entity
from data_snack.entities.entity_meta import EntityMetaClass
from data_snack.entities.exceptions import MetaFieldsException, MetaEmptyKeysException


@pytest.fixture
def dummy_entity() -> Type[Entity]:
    @dataclass
    class DummyEntity(Entity):
        key: int
        excluded: int
        included: int

        class Meta:
            keys: List[str] = ["key"]
            excluded_fields: List[str] = ["excluded"]
    return DummyEntity


def test_entity_init() -> None:

    meta_keys = ["key"]
    meta_excluded_fields = []

    @dataclass
    class DummyEntity(Entity):
        key: int
        included: int

        class Meta:
            keys: List[str] = meta_keys
            excluded_fields: List[str] = meta_excluded_fields

    assert type(DummyEntity) == EntityMetaClass
    assert DummyEntity.__bases__ == (Entity, )
    assert DummyEntity.Meta.keys == meta_keys
    assert DummyEntity.Meta.excluded_fields == meta_excluded_fields
    assert Entity.Meta.keys == []
    assert Entity.Meta.excluded_fields == []


def test_entity_init_bad_meta_fields_names() -> None:
    with pytest.raises(MetaFieldsException):
        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                bad_keys: List[str] = ["key"]
                bad_excluded_fields: List[str] = []


def test_entity_init_bad_meta_fields_types() -> None:
    with pytest.raises(MetaFieldsException):
        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                keys: List[int] = [1]
                excluded_fields: List[str] = []


def test_entity_init_empty_meta_keys() -> None:
    with pytest.raises(MetaEmptyKeysException):
        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                keys: List[str] = []
                excluded_fields: List[str] = []


def test_get_all_fields(dummy_entity) -> None:
    expected = ["key", "excluded", "included"]
    result = dummy_entity.get_all_fields()
    assert result == expected


def test_get_fields(dummy_entity) -> None:
    expected = ["key", "included"]
    result = dummy_entity.get_fields()
    assert result == expected


def test_get_excluded_fields(dummy_entity) -> None:
    expected = ["excluded"]
    result = dummy_entity.get_excluded_fields()
    assert result == expected


def test_get_keys(dummy_entity) -> None:
    expected = ["key"]
    result = dummy_entity.get_keys()
    assert result == expected
