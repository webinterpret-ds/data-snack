from dataclasses import dataclass
from typing import Dict, List, Text

from .base import Connection


@dataclass
class RedisConnection(Connection):
    connection: "Redis"

    def get(self, key: Text) -> bytes:
        return self.connection.get(key)

    def set(self, key: Text, value: Text, expire: int = 0) -> bool:
        ex = expire if expire > 0 else None
        return self.connection.set(key, value, ex=ex)

    def delete(self, key: Text) -> bool:
        n_deleted = self.connection.delete(key)
        return n_deleted == 1

    def get_many(self, keys: List[Text]) -> Dict[Text, bytes]:
        return dict(zip(keys, self.connection.mget(keys)))

    def set_many(self, values: Dict[Text, Text]) -> List[Text]:
        return self.connection.mset(values)

    def delete_many(self, keys: List[Text]) -> bool:
        n_deleted = self.connection.delete(*keys)
        return len(keys) == n_deleted

    def keys(self, pattern: Text) -> List[Text]:
        return self.connection.keys(pattern)
