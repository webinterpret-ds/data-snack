from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Type, Union

from ..entities import Entity


@dataclass
class Serializer(ABC):
    entity_type: Type[Entity]

    @abstractmethod
    def serialize(
        self, entity: Union[Entity, List[Entity]], many: bool = False
    ) -> Union[bytes, List[bytes]]:
        ...

    @abstractmethod
    def deserialize(
        self, data: Union[Optional[bytes], List[Optional[bytes]]], many: bool = False
    ) -> Union[Optional[Entity], List[Optional[Entity]]]:
        ...
