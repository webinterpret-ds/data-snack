from dataclasses import dataclass, field
from typing import Text, List, Optional, Type

from data_snack.entities import Entity
from .base import Wrap


@dataclass
class EntityWrap(Wrap):
    snack: "Snack"
    entity_type: Type[Entity]
    _entity_type_name: Text = field(init=False)

    @property
    def entity_type_name(self) -> Text:
        """Class name of the Entity used by the Wrap"""
        return self._entity_type_name

    def __post_init__(self):
        self._entity_type_name = self.entity_type.__name__

    def set(self, entity: Entity) -> Optional[Text]:
        return self.snack.set(entity)

    def get(self, key_values: List[Text]) -> Entity:
        return self.snack.get(self.entity_type, key_values)

    def get_many(self, keys_values: List[List[Text]]) -> List[Entity]:
        return self.snack.get_many(self.entity_type, keys_values)

    def set_many(self, entities: List[Entity]) -> List[Text]:
        return self.snack.set_many(entities)

    def keys(self) -> List[bytes]:
        return self.snack.keys(self.entity_type)
