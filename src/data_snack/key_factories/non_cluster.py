from data_snack.key_factories.base import Key


class NonClusterKey(Key):
    def get_pattern(self, pattern: str = "*") -> str:
        return f"{self.entity.__name__}-{pattern}"
