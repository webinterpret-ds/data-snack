from dataclasses import dataclass
from typing import Dict, List, Optional, Text
from data_snack.entities import Entity

from .base import Connection


@dataclass
class MemcachedConnection(Connection):
    connection: "Client"

    def get(self, entity_type: Type[Entity], key: Text) -> Optional[bytes]:
        return self.connection.get(key)

    def set(self, entity_type: Type[Entity], key: Text, value: Text, expire: int = 0) -> bool:
        return self.connection.set(key, value, expire=expire)

    def delete(self, entity_type: Type[Entity], key: Text) -> bool:
        return self.connection.delete(key, noreply=False)

    def get_many(self, entity_type: Type[Entity], keys: List[Text]) -> Dict[Text, Optional[bytes]]:
        return self.connection.get_many(keys)

    def set_many(self, entity_type: Type[Entity], values: Dict[Text, Text]) -> List[Text]:
        failed_keys = self.connection.set_many(values)
        return list(set(values.keys()) - set(failed_keys))

    def delete_many(
        self, entity_type: Type[Entity], keys: List[Text]
    ) -> bool:  # always returns True. How should we approach this?
        return self.connection.delete_many(keys, noreply=False)

    def keys(self, entity_type: Type[Entity], pattern: Text) -> List[Text]:
        raise NotImplementedError()
