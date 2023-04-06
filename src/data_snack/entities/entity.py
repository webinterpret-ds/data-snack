from abc import ABC
from dataclasses import dataclass
from typing import Any, List, get_type_hints

from data_snack.entities.entity_meta import EntityMetaClass


@dataclass
class Entity(ABC, metaclass=EntityMetaClass):
    def __init__(self, *args: Any, **kwargs: Any):
        ...

    class Meta:
        keys: List[str] = []
        excluded_fields: List[str] = []

    @classmethod
    def get_all_fields(cls) -> List[str]:
        """Gets all Entity fields."""
        return list(get_type_hints(cls))

    @classmethod
    def get_fields(cls) -> List[str]:
        """Gets Entity fields if not excluded."""
        return [
            field
            for field in cls.get_all_fields()
            if field not in cls.get_excluded_fields()
        ]

    @classmethod
    def get_excluded_fields(cls) -> List[str]:
        """Gets Entity excluded keys only."""
        return cls.Meta.excluded_fields

    @classmethod
    def get_keys(cls) -> List[str]:
        """Gets Entity keys only."""
        return cls.Meta.keys
