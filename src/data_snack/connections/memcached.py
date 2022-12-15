from dataclasses import dataclass
from typing import Text, Dict, List

from .base import Connection


@dataclass
class MemcachedConnection(Connection):
    connection: "Client"

    def get(self, key: Text) -> bytes:
        return self.connection.get(key)

    def set(self, key: Text, value: Text) -> bool:
        return self.connection.set(key, value)

    def delete(self, key: Text) -> bool:
        return self.connection.delete(key, noreply=False)

    def get_many(self, keys: List[Text]) -> Dict[Text, bytes]:
        return self.connection.get_many(keys)

    def set_many(self, values: Dict[Text, Text]) -> List[Text]:
        failed_keys = self.connection.set_many(values)
        return list(set(values.keys()) - set(failed_keys))

    def delete_many(self, keys: List[Text]) -> bool:  # always returns True. How should we approach this?
        return self.connection.delete_many(keys, noreply=False)

    def keys(self, pattern: Text) -> List[Text]:
        raise NotImplementedError()
