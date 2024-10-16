from dataclasses import dataclass
from typing import List, Dict

from data_snack.entities.base import Entity


@dataclass
class EntityFieldMapping:
    field: str
    source_field: str


@dataclass
class SourceEntity:
    entity: type(Entity)
    entity_fields_mapping: List[EntityFieldMapping]
    optional: bool

    def __post_init__(self):
        self._fields_mapping = {mapping.field: mapping.source_field for mapping in self.entity_fields_mapping}
        self._source_fields_mapping = {source_field: field for field, source_field in self._fields_mapping.items()}

    @property
    def fields_mapping(self) -> Dict[str, str]:
        return self._fields_mapping

    @property
    def source_fields_mapping(self) -> Dict[str, str]:
        return self._source_fields_mapping
