from data_snack.key_factories.base import KeyFactory
from dataclasses import dataclass
from hashlib import md5


def string_hash(value: str) -> str:
    return md5(value.encode()).hexdigest()


@dataclass
class HashKeyFactory(KeyFactory):
    def get_key(self, type_name: str, *key_values: str) -> str:
        return string_hash(f"{type_name}-{'_'.join(map(str, key_values))}")

    def get_pattern(self, type_name: str, pattern: str = "*") -> str:
        return None
