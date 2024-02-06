from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from data_snack.connections import Connection
from data_snack.key_factories import Key


@dataclass
class MemcachedConnection(Connection):
    connection: "Client"

    def get(self, key: Key) -> Optional[bytes]:
        return self.connection.get(key.keystring)

    def set(self, key: Key, value: str) -> bool:
        return self.connection.set(key.keystring, value)

    def delete(self, key: Key) -> bool:
        return self.connection.delete(key.keystring, noreply=False)

    def get_many(self, keys: List[Key]) -> Dict[str, Optional[bytes]]:
        keystrings = [key.keystring for key in keys]
        return self.connection.get_many(keystrings)

    def set_many(self, values: Dict[Key, Any]) -> List[Key]:
        keystrings_values = {}
        index_mapping = {}
        for index, (key, value) in enumerate(values.items()):
            keystrings_values[key.keystring] = value
            index_mapping[key.keystring] = index
        failed_keys = self.connection.set_many(keystrings_values)
        values_key_list = list(values.keys())
        return [
            values_key_list[index_mapping[keystring]] for keystring in keystrings_values if keystring not in failed_keys
        ]

    def delete_many(
        self, keys: List[Key]
    ) -> bool:  # always returns True. How should we approach this?
        keystrings = [key.keystring for key in keys]
        return self.connection.delete_many(keystrings, noreply=False)

    def keys(self, pattern: str) -> List[str]:
        raise NotImplementedError()
