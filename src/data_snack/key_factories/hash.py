from hashlib import md5

from data_snack.key_factories import Key


def string_hash(value: str) -> str:
    return md5(value.encode()).hexdigest()


class HashKey(Key):
    def get_pattern(self, pattern: str) -> str:
        return string_hash(f"{self.entity_type}-{pattern}")
