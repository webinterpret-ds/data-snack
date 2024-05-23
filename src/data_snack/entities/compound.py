from abc import ABC
from dataclasses import dataclass
from itertools import chain
from typing import List, Any

from data_snack.entities.entity_meta import CompoundEntityMetaClass
from data_snack.entities.models import SourceEntity
from data_snack.entities.utils import map_values, filter_missing_values


@dataclass
class CompoundEntity(ABC, metaclass=CompoundEntityMetaClass):
    def __init__(self, *args: Any, **kwargs: Any):
        ...

    class Meta:
        sources: List[SourceEntity] = []

    @classmethod
    def get_all_fields(cls) -> List[str]:
        """Gets all Entity fields."""
        return filter_missing_values(list(chain(*[
            map_values(source.source_fields_mapping, source.entity.get_all_fields())
            for source in cls.Meta.sources
        ])))

    @classmethod
    def get_fields(cls) -> List[str]:
        """Gets Entity fields if not excluded."""
        return filter_missing_values(list(chain(*[
            map_values(source.source_fields_mapping, source.entity.get_fields())
            for source in cls.Meta.sources
        ])))

    @classmethod
    def get_excluded_fields(cls) -> List[str]:
        """Gets Entity excluded keys only."""
        return filter_missing_values(list(chain(*[
            map_values(source.source_fields_mapping, source.entity.get_excluded_fields())
            for source in cls.Meta.sources
        ])))

    @classmethod
    def get_keys(cls) -> List[str]:
        """Gets Entity keys only."""
        return filter_missing_values(list(chain(*[
            map_values(source.source_fields_mapping, source.entity.get_keys())
            for source in cls.Meta.sources
        ])))
