from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type

from data_snack.entities import Entity


@dataclass
class Key(ABC):
    """An abstract key."""
    entity_type: Type[Entity]
    key_values: List[str]

    @abstractmethod
    def get_pattern(self, pattern: str) -> str:
        """
        Gets pattern string.
        :return: pattern string in specified format
        """
        pass

    @property
    def keystring(self) -> str:
        """
        Gets key string.
        :return: key string in specified format
        """
        return self.get_pattern('_'.join(map(str, self.key_values)))

