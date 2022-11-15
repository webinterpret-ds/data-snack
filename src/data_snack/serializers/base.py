from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union, List

from ..entities import EntityType, Entity


@dataclass
class Serializer(ABC):
    entity_type: EntityType

    @abstractmethod
    def serialize(self, entity: Union[Entity, List[Entity]], many: bool = False) -> Union[bytes, List[bytes]]:
        ...

    @abstractmethod
    def deserialize(self, data: Union[bytes, List[bytes]], many: bool = False) -> Union[Entity, List[Entity]]:
        ...
