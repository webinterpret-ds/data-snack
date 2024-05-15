from data_snack.key_factories.base import Key


class ClusterKey(Key):
    def get_pattern(self, pattern: str = "*") -> str:
        return f"{{{self.entity_type.__name__}-{self.entity_type.version}}}-{pattern}"
