from abc import ABC
from typing import Text, List, Optional, Any

from data_snack.entities import Entity


class Wrap(ABC):
    """
    Wraps are used to provide a simplified interface for accessing `Snack` for one, selected type of `Entity`.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        ...

    def set(self, entity: Entity) -> Optional[Text]:
        """
        Saves given entity in db.

        :param entity: an entity
        :return: a key to saved entity
        """
        ...

    def get(self, key_values: List[Text]) -> Entity:
        """
        Reads entities from db based on provided key values.

        :param key_values: a list of values from key fields
        :return: an entity retrieved from db
        """
        ...

    def get_many(self, keys_values: List[List[Text]]) -> List[Entity]:
        """
        Gets list of `Entity` objects from db based on provided list of keys.

        :param keys_values: a list of key values
        :return: a list of retrieved Entity objects.
        """
        ...

    def set_many(self, entities: List[Entity]) -> List[Text]:
        """
        Saves multiple `Entity` objects in db.

        :param entities: a list of Entity objects
        :return: a list of keys generated for saved objects
        """
        ...

    def keys(self) -> List[bytes]:
        """
        Reads a list of keys available in db for given `Entity` type.

        :return: a list of keys
        """
        ...
