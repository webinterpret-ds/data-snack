from dataclasses import dataclass
from typing import Text, List, Dict

from .base import Connection


@dataclass
class RedisConnection(Connection):
    connection: "Redis"

    def get(self, key: Text) -> bytes:
        return self.connection.get(key)

    def set(self, key: Text, value: Text) -> bool:
        return self.connection.set(key, value)

    def get_many(self, keys: List[Text]) -> Dict[Text, bytes]:
        return dict(zip(keys, self.connection.mget(keys)))

    def set_many(self, values: Dict[Text, Text]) -> List[Text]:
        return self.connection.mset(values)

    def keys(self, pattern: Text) -> List[Text]:
        return self.connection.keys(pattern)
