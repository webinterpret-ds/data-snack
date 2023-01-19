from abc import ABC
from dataclasses import dataclass
from typing import Any, List, get_type_hints, Type


@dataclass
class Entity(ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        ...

    class Meta:
        keys: List[str] = []
        excluded_fields: List[str] = []

    @classmethod
    @property
    def all_fields(cls: Type["Entity"]) -> List[str]:
        return list(get_type_hints(cls).keys())

    @classmethod
    @property
    def fields(cls: Type["Entity"]) -> List[str]:
        return list(set(cls.all_fields) - cls.Meta.excluded_fields)

    @classmethod
    @property
    def excluded_fields(cls: Type["Entity"]) -> List[str]:
        return cls.Meta.excluded_fields

    @classmethod
    @property
    def keys(cls: Type["Entity"]) -> List[str]:
        return cls.Meta.keys
