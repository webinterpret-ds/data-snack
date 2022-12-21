from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Text, List, Optional, Any, Type, Protocol

from data_snack.entities import Entity


class SnackProtocol(Protocol):
    def set(self, entity: Entity) -> Optional[Text]:
        ...

    def get(self, cls: Type[Entity], key_values: List[Text]) -> Entity:
        ...

    def get_many(self, cls: Type[Entity], keys_values: List[List[Text]]) -> List[Entity]:
        ...

    def set_many(self, entities: List[Entity]) -> List[Text]:
        ...

    def keys(self, cls: Type[Entity]) -> List[bytes]:
        ...


@dataclass
class Wrap(ABC):
    """
    Wraps are used to provide a simplified interface for accessing `Snack` for one, selected type of `Entity`.
    """
    snack: SnackProtocol
    entity_type: Type[Entity]

    @abstractmethod
    def set(self, entity: Entity) -> Optional[Text]:
        """
        Saves given entity in db.

        :param entity: an entity
        :return: a key to saved entity
        """
        ...

    @abstractmethod
    def get(self, key_values: List[Text]) -> Entity:
        """
        Reads entities from db based on provided key values.

        :param key_values: a list of values from key fields
        :return: an entity retrieved from db
        """
        ...

    @abstractmethod
    def get_many(self, keys_values: List[List[Text]]) -> List[Entity]:
        """
        Gets list of `Entity` objects from db based on provided list of keys.

        :param keys_values: a list of key values
        :return: a list of retrieved Entity objects.
        """
        ...

    @abstractmethod
    def set_many(self, entities: List[Entity]) -> List[Text]:
        """
        Saves multiple `Entity` objects in db.

        :param entities: a list of Entity objects
        :return: a list of keys generated for saved objects
        """
        ...

    @abstractmethod
    def keys(self) -> List[bytes]:
        """
        Reads a list of keys available in db for given `Entity` type.

        :return: a list of keys
        """
        ...
