from abc import ABCMeta, ABC

from .exceptions import MetaFieldsException, MetaEmptyKeysException, NonExistingMetaError


class EntityMetaClass(ABCMeta):

    meta_fields = ["keys", "excluded_fields"]

    def __new__(mcs, name, bases, dct):
        entity_class = super().__new__(mcs, name, bases, dct)
        # TODO: consider encapsulation of each validation rule to function to make this class cleaner.
        if not entity_class.__dict__.get("Meta"):
            raise NonExistingMetaError(f"Private class `Meta not defined for {entity_class.__name__}.")
        if bases != (ABC, ):
            if missing_fields := [field for field in mcs.meta_fields if field not in entity_class.Meta.__dict__]:
                raise MetaFieldsException(f"Missing Meta fields: {missing_fields}.")
            if not entity_class.Meta.keys:
                raise MetaEmptyKeysException("Meta keys can not be empty.")
        return entity_class
