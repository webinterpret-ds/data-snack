from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from data_snack.connections import Connection
from data_snack.key_factories import Key


@dataclass
class RedisConnection(Connection):
    connection: "Redis"

    def get(self, key: Key) -> Optional[bytes]:
        return self.connection.get(key.keystring)

    def set(self, key: Key, value: str, expire: int = 0) -> bool:
        ex = expire if expire > 0 else None
        return self.connection.set(key.keystring, value, ex=ex)

    def delete(self, key: Key) -> bool:
        n_deleted = self.connection.delete(key.keystring)
        return n_deleted == 1

    def get_many(self, keys: List[Key]) -> Dict[str, Optional[bytes]]:
        keystrings = [key.keystring for key in keys]
        return dict(zip(keystrings, self.connection.mget(keystrings)))

    def set_many(self, values: Dict[Key, str]) -> Any:
        # TODO: values.values type is not str probably
        values = {key.keystring: value for (key, value) in values.items()}
        return self.connection.mset(values)

    def delete_many(self, keys: List[Key]) -> bool:
        n_deleted = self.connection.delete(*[key.keystring for key in keys])
        return len(keys) == n_deleted

    def keys(self, pattern: str) -> List[str]:
        return self.connection.keys(pattern)
