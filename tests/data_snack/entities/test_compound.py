from abc import ABC
from dataclasses import dataclass
from typing import Type

import pytest

from data_snack.entities import CompoundEntity, Entity
from data_snack.entities.entity_meta import CompoundEntityMetaClass
from data_snack.entities.exceptions import (
    MetaFieldsException,
    NonExistingMetaError,
    MetaEmptyKeysException,
    SourceEntityFieldException,
    DuplicatedFieldsException,
)
from data_snack.entities.models import SourceEntity, EntityFieldMapping


def test_compound_entity_type() -> None:
    """Testing if `CompoundEntity` has proper type."""
    assert type(CompoundEntity) == CompoundEntityMetaClass


def test_compound_entity_bases() -> None:
    """Testing if `CompoundEntity` has proper bases."""
    assert CompoundEntity.__bases__ == (ABC,)


def test_compound_entity_subclass_init() -> None:
    """
    Testing if `CompoundEntity` subclasses are initialized properly (type, bases, structure),
    and if initialization doesn't product unwanted side effects.
    """
    @dataclass
    class DummyEntity(Entity):
        key: int

        class Meta:
            keys = ["key"]
            excluded_fields = []
            version = 1

    meta_sources = [
        SourceEntity(
            entity=DummyEntity,
            entity_fields_mapping=[
                EntityFieldMapping(field="key", source_field="key")
            ]
        )
    ]

    @dataclass
    class DummyCompoundEntity(CompoundEntity):
        key: int

        class Meta:
            sources = meta_sources

    assert type(DummyCompoundEntity) == CompoundEntityMetaClass
    assert DummyCompoundEntity.__bases__ == (CompoundEntity,)
    assert DummyCompoundEntity.Meta.sources == meta_sources
    assert CompoundEntity.Meta.sources == []


def test_compound_entity_init_no_meta_defined() -> None:
    """Testing error handling if `CompoundEntity` does not provide `Meta` implementation."""
    with pytest.raises(NonExistingMetaError):

        @dataclass
        class CompoundEntityNoMeta(ABC, metaclass=CompoundEntityMetaClass):
            pass


def test_compound_entity_subclass_init_bad_meta_fields_names() -> None:
    """Testing compound entity subclasses `Meta` field names validation."""
    with pytest.raises(MetaFieldsException):

        @dataclass
        class DummyEntity(Entity):
            key: int

            class Meta:
                keys = ["key"]
                excluded_fields = []
                version = 1

        @dataclass
        class DummyCompoundEntity(CompoundEntity):
            key: int

            class Meta:
                bad_sources = [
                    SourceEntity(
                        entity=DummyEntity,
                        entity_fields_mapping=[
                            EntityFieldMapping(field="key", source_field="key")
                        ]
                    )
                ]


def test_compound_entity_subclass_init_empty_meta_sources() -> None:
    """Testing compound entity subclasses `Meta` field content validation."""
    with pytest.raises(MetaEmptyKeysException):

        @dataclass
        class CompoundDummyEntity(CompoundEntity):
            key: int

            class Meta:
                sources = []


def test_compound_entity_sources_keys_no_defined() -> None:
    """Testing compound entity all sources keys mappings validation."""
    with pytest.raises(SourceEntityFieldException):

        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                keys = ["key"]
                excluded_fields = []
                version = 1

        @dataclass
        class CompoundDummyEntity(CompoundEntity):
            included: int

            class Meta:
                sources = [
                    SourceEntity(
                        entity=DummyEntity,
                        entity_fields_mapping=[
                            EntityFieldMapping(field="included", source_field="included")
                        ]
                    )
                ]


def test_compound_entity_sources_fields_no_mapped() -> None:
    """Testing compound entity all sources fields mappings validation."""
    with pytest.raises(SourceEntityFieldException):
        @dataclass
        class DummyEntity(Entity):
            key: int

            class Meta:
                keys = ["key"]
                excluded_fields = []
                version = 1

        @dataclass
        class CompoundDummyEntity(CompoundEntity):
            key: int
            included: int

            class Meta:
                sources = [
                    SourceEntity(
                        entity=DummyEntity,
                        entity_fields_mapping=[
                            EntityFieldMapping(field="key", source_field="key"),
                            EntityFieldMapping(field="included", source_field="included")
                        ]
                    )
                ]


def test_compound_entity_duplicated_field_between_source_entities() -> None:
    """Testing compound entity all fields between source entities unique."""
    with pytest.raises(DuplicatedFieldsException):
        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                keys = ["key"]
                excluded_fields = []
                version = 1

        @dataclass
        class AnotherDummyEntity(Entity):
            another_key: int
            another_included: int

            class Meta:
                keys = ["another_key"]
                excluded_fields = []
                version = 1

        @dataclass
        class CompoundDummyEntity(CompoundEntity):
            key: int
            another_key: int
            included: int

            class Meta:
                sources = [
                    SourceEntity(
                        entity=DummyEntity,
                        entity_fields_mapping=[
                            EntityFieldMapping(field="key", source_field="key"),
                            EntityFieldMapping(field="included", source_field="included")
                        ]
                    ),
                    SourceEntity(
                        entity=AnotherDummyEntity,
                        entity_fields_mapping=[
                            EntityFieldMapping(field="another_key", source_field="another_key"),
                            EntityFieldMapping(field="included", source_field="another_included")
                        ]
                    )
                ]


def test_compound_entity_duplicated_key_between_source_entities() -> None:
    """Testing compound entity duplicated key between source entities."""
    @dataclass
    class DummyEntity(Entity):
        key: int
        included: int

        class Meta:
            keys = ["key"]
            excluded_fields = []
            version = 1

    @dataclass
    class AnotherDummyEntity(Entity):
        another_key: int
        another_included: int

        class Meta:
            keys = ["another_key"]
            excluded_fields = []
            version = 1

    @dataclass
    class CompoundDummyEntity(CompoundEntity):
        key: int
        included: int
        another_included: int

        class Meta:
            sources = [
                SourceEntity(
                    entity=DummyEntity,
                    entity_fields_mapping=[
                        EntityFieldMapping(field="key", source_field="key"),
                        EntityFieldMapping(field="included", source_field="included")
                    ]
                ),
                SourceEntity(
                    entity=AnotherDummyEntity,
                    entity_fields_mapping=[
                        EntityFieldMapping(field="key", source_field="another_key"),
                        EntityFieldMapping(field="another_included", source_field="another_included")
                    ]
                )
            ]


def test_compound_entity_duplicated_source_entity_field() -> None:
    """Testing compound entity all fields in source entity unique."""
    with pytest.raises(DuplicatedFieldsException):
        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int
            another_included: int

            class Meta:
                keys = ["key"]
                excluded_fields = []
                version = 1

        @dataclass
        class CompoundDummyEntity(CompoundEntity):
            key: int
            included: int

            class Meta:
                sources = [
                    SourceEntity(
                        entity=DummyEntity,
                        entity_fields_mapping=[
                            EntityFieldMapping(field="key", source_field="key"),
                            EntityFieldMapping(field="included", source_field="included"),
                            EntityFieldMapping(field="included", source_field="another_included")
                        ]
                    )
                ]


def test_compound_entity_duplicated_source_entity_source_field() -> None:
    """Testing compound entity all source fields in source entity unique."""
    with pytest.raises(DuplicatedFieldsException):
        @dataclass
        class DummyEntity(Entity):
            key: int
            included: int

            class Meta:
                keys = ["key"]
                excluded_fields = []
                version = 1

        @dataclass
        class CompoundDummyEntity(CompoundEntity):
            key: int
            included: int
            another_included: int

            class Meta:
                sources = [
                    SourceEntity(
                        entity=DummyEntity,
                        entity_fields_mapping=[
                            EntityFieldMapping(field="key", source_field="key"),
                            EntityFieldMapping(field="included", source_field="included"),
                            EntityFieldMapping(field="another_included", source_field="included")
                        ]
                    )
                ]


def test_compound_get_all_fields(dummy_compound_entity: Type[CompoundEntity]) -> None:
    """Testing if `get_all_fields` returns all fields indeed."""
    expected = ["key", "excluded", "included", "another_key", "another_excluded", "another_included"]
    result = dummy_compound_entity.get_all_fields()
    assert result == expected


def test_compound_get_fields(dummy_compound_entity: Type[CompoundEntity]) -> None:
    """Testing if `get_fields` filters out `Meta.excluded_fields`."""
    expected = ["key", "included", "another_key", "another_included"]
    result = dummy_compound_entity.get_fields()
    assert result == expected


def test_compound_get_excluded_fields(dummy_compound_entity: Type[CompoundEntity]) -> None:
    """Testing if `get_excluded_fields` returns `Meta.excluded_fields`."""
    expected = ["excluded", "another_excluded"]
    result = dummy_compound_entity.get_excluded_fields()
    assert result == expected


def test_compound_get_keys(dummy_compound_entity: Type[CompoundEntity]) -> None:
    """Testing if get_keys returns `Meta.keys`."""
    expected = ["key", "another_key"]
    result = dummy_compound_entity.get_keys()
    assert result == expected
