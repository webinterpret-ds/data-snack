from itertools import chain

from data_snack.entities.exceptions import (
    NonExistingMetaError,
    MetaFieldsException,
    MetaEmptyKeysException,
    SourceEntityFieldException,
)


def validate_meta_class(entity_class) -> None:
    if "Meta" not in dir(entity_class):
        raise NonExistingMetaError(
            f"Private class `Meta not defined for {entity_class.__name__}."
        )


def validate_meta_fields(entity_class, meta_fields) -> None:
    if missing_fields := [
        field
        for field in meta_fields
        if field not in dir(entity_class.Meta)
    ]:
        raise MetaFieldsException(f"Missing Meta fields: {missing_fields}.")


def validate_meta_keys(entity_class) -> None:
    if not entity_class.Meta.keys:
        raise MetaEmptyKeysException("Meta keys can not be empty.")


def validate_meta_sources(entity_class) -> None:
    if not entity_class.Meta.sources:
        raise MetaEmptyKeysException("Meta sources can not be empty.")


def validate_meta_sources_keys(entity_class) -> None:
    if missing_keys := list(chain(*[
        [
            f"{source.entity.__name__}.{key}"
            for key in source.entity.get_keys()
            if key not in source.source_fields_mapping.keys()
        ]
        for source in entity_class.Meta.sources
    ])):
        raise SourceEntityFieldException(f"Missing source entity keys: {missing_keys}.")


def validate_meta_sources_fields(entity_class) -> None:
    if missing_mappings := list(chain(*[
        [
            f"{source.entity.__name__}.{field}"
            for field in source.source_fields_mapping.keys()
            if field not in source.entity.get_all_fields()
        ]
        for source in entity_class.Meta.sources
    ])):
        raise SourceEntityFieldException(f"Missing source entity fields: {missing_mappings}.")
