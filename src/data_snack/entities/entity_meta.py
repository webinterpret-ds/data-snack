from abc import ABCMeta, ABC
from typing import List, get_type_hints

from data_snack.entities.exceptions import MetaFieldsException, MetaEmptyKeysException


class EntityMetaClass(ABCMeta):

    class Meta:
        keys: List[str] = []
        excluded_fields: List[str] = []

    def __new__(mcs, name, bases, dct):
        entity_class = super().__new__(mcs, name, bases, dct)
        if (available_fields := get_type_hints(mcs.Meta)) != (defined_fields := get_type_hints(entity_class.Meta)):
            raise MetaFieldsException(
                f"Meta available fields are: \n{available_fields}, while defined fields are: \n{defined_fields}."
            )
        if entity_class.__bases__ != (ABC, ) and not entity_class.Meta.keys:
            raise MetaEmptyKeysException("Meta keys can not be empty.")
        return entity_class
