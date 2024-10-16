from abc import ABC
from collections import ChainMap
from dataclasses import dataclass
from itertools import chain
from typing import List, Any, Optional

from data_snack.entities import Entity
from data_snack.entities.entity_meta import CompoundEntityMetaClass
from data_snack.entities.models import SourceEntity, EntityFieldMapping
from data_snack.entities.utils import map_values, filter_missing_values, get_unique_values


_filter_mapped_values = lambda mapping, fields: filter_missing_values(map_values(mapping, fields))


@dataclass
class CompoundEntity(ABC, metaclass=CompoundEntityMetaClass):
    def __init__(self, *args: Any, **kwargs: Any):
        ...

    class Meta:
        sources: List[SourceEntity] = []

    @classmethod
    def get_all_fields(cls) -> List[str]:
        """Gets all CompoundEntity fields."""
        return get_unique_values(list(chain(*[
            _filter_mapped_values(source.source_fields_mapping, source.entity.get_all_fields())
            for source in cls.Meta.sources
        ])))

    @classmethod
    def get_fields(cls) -> List[str]:
        """Gets CompoundEntity fields if not excluded."""
        return get_unique_values(list(chain(*[
            _filter_mapped_values(source.source_fields_mapping, source.entity.get_fields())
            for source in cls.Meta.sources
        ])))

    @classmethod
    def get_excluded_fields(cls) -> List[str]:
        """Gets CompoundEntity excluded keys only."""
        return get_unique_values(list(chain(*[
            _filter_mapped_values(source.source_fields_mapping, source.entity.get_excluded_fields())
            for source in cls.Meta.sources
        ])))

    @classmethod
    def get_keys(cls) -> List[str]:
        """Gets CompoundEntity keys only."""
        return get_unique_values(list(chain(*[
            _filter_mapped_values(source.source_fields_mapping, source.entity.get_keys())
            for source in cls.Meta.sources
        ])))

    @classmethod
    def create_from_source_entities(
        cls,
        entities: List[Optional[Entity]],
        entities_field_mappings: List[List[EntityFieldMapping]],
        key_values: List[Any]
    ) -> "CompoundEntity":
        """Creates CompoundEntity from source entities."""
        keys_with_values = dict(zip(cls.get_keys(), key_values))
        empty_fields = dict.fromkeys(cls.get_all_fields())
        fields_with_values = dict(ChainMap(*[
            {mapping.field: getattr(entity, mapping.source_field) for mapping in entity_fields_mapping}
            for entity, entity_fields_mapping in zip(entities, entities_field_mappings) if entity
        ]))
        return cls(**{**empty_fields, **fields_with_values, **keys_with_values})
