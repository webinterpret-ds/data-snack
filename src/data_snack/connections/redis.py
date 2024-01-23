from dataclasses import dataclass
from typing import Dict, List, Optional
from data_snack.entities import Entity

from .base import Connection


@dataclass
class RedisConnection(Connection):
    connection: "Redis"

    def get(self, entity_type: Type[Entity], key: str) -> Optional[bytes]:
        return self.connection.get(key)

    def set(self, entity_type: Type[Entity], key: str, value: str, expire: int = 0) -> bool:
        ex = expire if expire > 0 else None
        return self.connection.set(key, value, ex=ex)

    def delete(self, entity_type: Type[Entity], key: str) -> bool:
        n_deleted = self.connection.delete(key)
        return n_deleted == 1

    def get_many(self, entity_type: Type[Entity], keys: List[str]) -> Dict[str, Optional[bytes]]:
        return dict(zip(keys, self.connection.mget(keys)))

    def set_many(self, entity_type: Type[Entity], values: Dict[str, str]) -> List[str]:
        return self.connection.mset(values)

    def delete_many(self, entity_type: Type[Entity], keys: List[str]) -> bool:
        n_deleted = self.connection.delete(*keys)
        return len(keys) == n_deleted

    def keys(self, entity_type: Type[Entity], pattern: str) -> List[str]:
        return self.connection.keys(pattern)
