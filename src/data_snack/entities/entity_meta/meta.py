from abc import ABCMeta, ABC
from dataclasses import is_dataclass
from typing import List, get_type_hints

from .exceptions import MetaFieldsException, MetaEmptyKeysException, NonExistingMetaError


class EntityMetaClass(ABCMeta):

    meta_structure = {
        "keys": List[str],
        "excluded_fields": List[str]
    }

    def __new__(mcs, name, bases, dct):
        entity_class = super().__new__(mcs, name, bases, dct)
        try:
            entity_class.Meta
        except AttributeError:
            raise NonExistingMetaError(f"Private class `Meta not defined for {entity_class.__name__}.")
        if bases != (ABC, ):
            if not is_dataclass(entity_class):
                raise TypeError(f"{entity_class.__name__} is not well defined dataclass.")
            if mcs.meta_structure != (defined_fields := get_type_hints(entity_class.Meta)):
                raise MetaFieldsException(
                    f"Meta available fields are: \n{mcs.meta_structure}, while defined fields are: \n{defined_fields}."
                )
            if not entity_class.Meta.keys:
                raise MetaEmptyKeysException("Meta keys can not be empty.")
        return entity_class
