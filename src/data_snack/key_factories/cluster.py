from data_snack.key_factories.base import Key


class ClusterKey(Key):
    def get_pattern(self, pattern: str = "*") -> str:
        return f"{{{self.entity.__name__}}}-{pattern}"
