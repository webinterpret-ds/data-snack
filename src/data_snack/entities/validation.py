from abc import ABCMeta
from collections import Counter, defaultdict
from itertools import chain
from typing import List

from data_snack.entities.exceptions import (
    NonExistingMetaError,
    MetaFieldsException,
    MetaEmptyKeysException,
    SourceEntityFieldException,
    DuplicatedFieldsException,
)


def validate_meta_class(entity_class: ABCMeta) -> None:
    """
    Validates if entity contains 'Meta' private class.
    :param entity_class: entity to validate
    """
    try:
        getattr(entity_class, "Meta")
    except AttributeError:
        raise NonExistingMetaError(
            f"Private class `Meta not defined for {entity_class.__name__}."
        )


def validate_meta_fields(entity_class: ABCMeta, meta_fields: List[str]) -> None:
    """
    Validates if entity 'Meta' private class has all fields defined.
    :param entity_class: entity to validate
    :param meta_fields: 'Meta' class fields list
    """
    missing_fields = []
    for field in meta_fields:
        try:
            getattr(entity_class.Meta, field)
        except AttributeError:
            missing_fields.append(field)
    if missing_fields:
        raise MetaFieldsException(f"Missing Meta fields: {missing_fields}.")


def validate_meta_keys(entity_class: ABCMeta) -> None:
    """
    Validates if 'keys' field of entity 'Meta' private class is not empty.
    :param entity_class: entity to validate
    """
    if not entity_class.Meta.keys:
        raise MetaEmptyKeysException("Meta keys can not be empty.")


def validate_meta_sources(entity_class: ABCMeta) -> None:
    """
    Validates if 'sources' field of entity 'Meta' private class is not empty.
    :param entity_class: entity to validate
    """
    if not entity_class.Meta.sources:
        raise MetaEmptyKeysException("Meta sources can not be empty.")


def validate_meta_sources_keys(entity_class: ABCMeta) -> None:
    """
    Validates if all source entities keys are defined in entity.
    :param entity_class: entity to validate
    """
    if missing_keys := list(chain(*[
        [
            f"{source.entity.__name__}.{key}"
            for key in source.entity.get_keys()
            if key not in source.source_fields_mapping.keys()
        ]
        for source in entity_class.Meta.sources
    ])):
        raise SourceEntityFieldException(f"Missing source entity keys: {missing_keys}.")


def validate_meta_sources_fields(entity_class: ABCMeta) -> None:
    """
    Validates if all fields defined in entity have mappings to fields from the source entities.
    :param entity_class: entity to validate
    """
    if missing_mappings := list(chain(*[
        [
            f"{source.entity.__name__}.{field}"
            for field in source.source_fields_mapping.keys()
            if field not in source.entity.get_all_fields()
        ]
        for source in entity_class.Meta.sources
    ])):
        raise SourceEntityFieldException(f"Missing source entity fields: {missing_mappings}.")


def validate_unique_fields_between_source_entities(entity_class: ABCMeta) -> None:
    """
    Validates if there are no duplicated fields between source entities except their keys.
    :param entity_class: entity to validate
    """
    fields_count = defaultdict(lambda: 0)
    for source in entity_class.Meta.sources:
        _source_keys = source.entity.get_keys()
        for mapping in source.entity_fields_mapping:
            if mapping.source_field not in _source_keys:
                fields_count[mapping.field] += 1

    if duplicated_fields := [f for (f, c) in fields_count.items() if c > 1]:
        raise DuplicatedFieldsException(f"Duplicated fields between source entities: {duplicated_fields}")


def validate_unique_source_entities_fields(entity_class: ABCMeta) -> None:
    """
    Validates if there are no duplicated fields in source entities.
    :param entity_class: entity to validate
    """
    if duplicated_source_fields := list(chain(*[
        [
            f"{source.entity.__name__}.{duplicated_field}"
            for duplicated_field, count in Counter(
                [
                    mapping.field
                    for mapping in source.entity_fields_mapping
                ]
            ).items() if count > 1
        ]
        for source in entity_class.Meta.sources
    ])):
        raise DuplicatedFieldsException(f"Duplicated fields in source entities: {duplicated_source_fields}")


def validate_unique_source_entities_source_fields(entity_class: ABCMeta) -> None:
    """
    Validates if there are no duplicated source fields in source entities.
    :param entity_class: entity to validate
    """
    if duplicated_source_fields := list(chain(*[
        [
            f"{source.entity.__name__}.{duplicated_source_field}"
            for duplicated_source_field, count in Counter(
                [
                    mapping.source_field
                    for mapping in source.entity_fields_mapping
                ]
            ).items() if count > 1
        ]
        for source in entity_class.Meta.sources
    ])):
        raise DuplicatedFieldsException(f"Duplicated source fields in source entities: {duplicated_source_fields}")

