from dataclasses import dataclass
from typing import Type, List

import pytest
from data_snack.entities import Entity, CompoundEntity
from data_snack.entities.models import SourceEntity, EntityFieldMapping


@pytest.fixture
def dummy_entity() -> Type[Entity]:
    @dataclass
    class DummyEntity(Entity):
        key: int
        excluded: int
        included: int

        class Meta:
            keys = ["key"]
            excluded_fields = ["excluded"]
            version = 1

    return DummyEntity


@pytest.fixture
def another_dummy_entity() -> Type[Entity]:
    @dataclass
    class AnotherDummyEntity(Entity):
        key: int
        another_key: int
        another_excluded: int
        another_included: int

        class Meta:
            keys = ["key", "another_key"]
            excluded_fields = ["another_excluded"]
            version = 1

    return AnotherDummyEntity


@pytest.fixture
def dummy_entity_fields_mapping() -> List[EntityFieldMapping]:
    return [
        EntityFieldMapping(field="key", source_field="key"),
        EntityFieldMapping(field="excluded", source_field="excluded"),
        EntityFieldMapping(field="included", source_field="included"),
    ]


@pytest.fixture
def another_dummy_entity_fields_mapping() -> List[EntityFieldMapping]:
    return [
        EntityFieldMapping(field="key", source_field="key"),
        EntityFieldMapping(field="another_key", source_field="another_key"),
        EntityFieldMapping(field="another_excluded", source_field="another_excluded"),
        EntityFieldMapping(field="another_included", source_field="another_included"),
    ]


@pytest.fixture
def dummy_compound_entity(
    dummy_entity: Type[Entity],
    dummy_entity_fields_mapping: List[EntityFieldMapping],
    another_dummy_entity: Type[Entity],
    another_dummy_entity_fields_mapping: List[EntityFieldMapping]
) -> Type[CompoundEntity]:
    @dataclass
    class DummyCompoundEntity(CompoundEntity):
        key: int
        excluded: int
        included: int
        another_key: int
        another_excluded: int
        another_included: int

        class Meta:
            sources = [
                SourceEntity(
                    entity=dummy_entity,
                    entity_fields_mapping=dummy_entity_fields_mapping,
                    optional=False
                ),
                SourceEntity(
                    entity=another_dummy_entity,
                    entity_fields_mapping=another_dummy_entity_fields_mapping,
                    optional=False
                )
            ]

    return DummyCompoundEntity
