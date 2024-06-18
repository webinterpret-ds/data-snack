from abc import ABC, ABCMeta

from data_snack.entities.validation import (
    validate_meta_class,
    validate_meta_fields,
    validate_meta_keys,
    validate_meta_sources,
    validate_meta_sources_fields,
    validate_meta_sources_keys,
    validate_unique_fields_between_source_entities,
    validate_unique_source_entities_fields,
    validate_unique_source_entities_source_fields,
)


class MetaClass(ABCMeta):

    def __new__(mcs, name, bases, dct):
        entity_class = super().__new__(mcs, name, bases, dct)
        validate_meta_class(entity_class)
        return entity_class


class EntityMetaClass(MetaClass):

    meta_fields = ["keys", "excluded_fields", "version"]

    def __new__(mcs, name, bases, dct):
        entity_class = super().__new__(mcs, name, bases, dct)
        if bases != (ABC,):
            validate_meta_fields(entity_class, mcs.meta_fields)
            validate_meta_keys(entity_class)
        return entity_class


class CompoundEntityMetaClass(MetaClass):

    meta_fields = ["sources"]

    def __new__(mcs, name, bases, dct):
        entity_class = super().__new__(mcs, name, bases, dct)
        if bases != (ABC,):
            validate_meta_fields(entity_class, mcs.meta_fields)
            validate_meta_sources(entity_class)
            validate_meta_sources_keys(entity_class)
            validate_meta_sources_fields(entity_class)
            validate_unique_source_entities_fields(entity_class)
            validate_unique_source_entities_source_fields(entity_class)
            validate_unique_fields_between_source_entities(entity_class)
        return entity_class
