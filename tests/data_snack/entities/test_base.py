from abc import ABC
from dataclasses import dataclass
from typing import Type

import pytest

from data_snack.entities import Entity
from data_snack.entities.entity_meta import EntityMetaClass
from data_snack.entities.exceptions import (
    MetaEmptyKeysException,
    MetaFieldsException,
    NonExistingMetaError,
)


def test_entity_type() -> None:
    """Testing if `Entity` has proper type."""
    assert type(Entity) == EntityMetaClass


def test_entity_bases() -> None:
    """Testing if `Entity` has proper bases."""
    assert Entity.__bases__ == (ABC,)


def test_entity_subclass_init() -> None:
    """
    Testing if `Entity` subclasses are initialized properly (type, bases, structure), and if initialization doesn't
    product unwanted side effects.
    """

    meta_keys = ["key"]
    meta_excluded_fields = []

    @dataclass
    class DummyEntity(Entity):
        key: int
        included: int

        class Meta:
            keys = meta_keys
            excluded_fields = meta_excluded_fields
            version = 1

    assert type(DummyEntity) == EntityMetaClass
    assert DummyEntity.__bases__ == (Entity,)
    assert DummyEntity.Meta.keys == meta_keys
    assert DummyEntity.Meta.excluded_fields == meta_excluded_fields
    assert DummyEntity.version == 1
    assert Entity.Meta.keys == []
    assert Entity.Meta.excluded_fields == []


def test_entity_subclass_init_bad_meta_fields_names() -> None:
    """Testing entity subclasses `Meta` field names validation."""
    with pytest.raises(MetaFieldsException):

        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                bad_keys = ["key"]
                bad_excluded_fields = []
                version = 1


def test_entity_subclass_init_empty_meta_keys() -> None:
    """Testing entity subclasses `Meta` field content validation."""
    with pytest.raises(MetaEmptyKeysException):

        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                keys = []
                excluded_fields = []
                version = 1


def test_entity_init_no_meta_defined() -> None:
    """Testing error handling if `Entity` does not provide `Meta` implementation."""

    with pytest.raises(NonExistingMetaError):

        @dataclass
        class EntityNoMeta(ABC, metaclass=EntityMetaClass):
            pass


def test_get_all_fields(dummy_entity: Type[Entity]) -> None:
    """Testing if `get_all_fields` returns all fields indeed."""
    expected = ["key", "excluded", "included"]
    result = dummy_entity.get_all_fields()
    assert result == expected


def test_get_fields(dummy_entity: Type[Entity]) -> None:
    """Testing if `get_fields` filters out `Meta.excluded_fields`."""
    expected = ["key", "included"]
    result = dummy_entity.get_fields()
    assert result == expected


def test_get_excluded_fields(dummy_entity: Type[Entity]) -> None:
    """Testing if `get_excluded_fields` returns `Meta.excluded_fields`."""
    expected = ["excluded"]
    result = dummy_entity.get_excluded_fields()
    assert result == expected


def test_get_keys(dummy_entity: Type[Entity]) -> None:
    """Testing if get_keys returns `Meta.keys`."""
    expected = ["key"]
    result = dummy_entity.get_keys()
    assert result == expected
