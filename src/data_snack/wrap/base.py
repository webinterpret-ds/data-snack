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

    def get(self, key: List[Text]) -> Entity:
        """
        Reads entities from db based on provided keys.

        :param key: a key
        :return: an entity retrieved from db
        """
        ...

    def get_many(self, keys: List[List[Text]]) -> List[Entity]:
        ...

    def set_many(self, entities: List[Entity]) -> List[Text]:
        ...

    def keys(self) -> List[bytes]:
        ...
