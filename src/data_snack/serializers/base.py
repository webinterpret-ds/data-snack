from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union, List, Type

from ..entities import Entity


@dataclass
class Serializer(ABC):
    entity_type: Type[Entity]

    @abstractmethod
    def serialize(self, entity: Union[Entity, List[Entity]], many: bool = False) -> Union[bytes, List[bytes]]:
        ...

    @abstractmethod
    def deserialize(self, data: Union[bytes, List[bytes]], many: bool = False) -> Union[Entity, List[Entity]]:
        ...
