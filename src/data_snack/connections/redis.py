from dataclasses import dataclass
from typing import Text, List, Dict

from .base import Connection


@dataclass
class RedisConnection(Connection):
    connection: "Redis"

    def get(self, key: Text):
        return self.connection.get(key)

    def set(self, key: Text, value: Text):
        return self.connection.set(key, value)

    def get_many(self, keys: List[Text]) -> Dict[Text, bytes]:
        return dict(zip(keys, self.connection.mget(keys)))

    def set_many(self, values: Dict[Text, Text]):
        return self.connection.mset(values)

    def keys(self, pattern: Text) -> List[bytes]:
        return self.connection.keys(pattern)
