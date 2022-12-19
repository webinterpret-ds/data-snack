from typing import Protocol, Text


class KeyFactory(Protocol):
    def __call__(self, type_name: Text, *key_values: Text) -> Text:
        ...


def key_factory(type_name: Text, *key_values: Text) -> Text:
    return f"{type_name}-{'_'.join(key_values)}"


def key_factory_cluster(type_name: Text, *key_values: Text) -> Text:
    return f"{{{type_name}}}-{'_'.join(key_values)}"
