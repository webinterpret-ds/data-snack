from abc import ABC
from typing import Text


class BaseKeyFactory(ABC):
    """
    KeyFactory is used to get key strings and their pattern
    """

    def get_key(self, type_name: Text, *key_values: Text) -> Text:
        """
        Gets key string.

        :param type_name: type name
        :param key_values: key values
        :return: key string in specified format
        """
        ...

    def get_pattern(self, type_name: Text) -> Text:
        """
        Gets pattern string.

        :param type_name: type name
        :return: pattern string in specified format
        """
        ...


class SingleKeyFactory(BaseKeyFactory):
    def get_key(self, type_name: Text, *key_values: Text) -> Text:

        return f"{type_name}-{'_'.join(map(str, key_values))}"

    def get_pattern(self, type_name: Text) -> Text:
        return f"{type_name}-*"


class ClusterKeyFactory(BaseKeyFactory):
    def get_key(self, type_name: Text, *key_values: Text) -> Text:
        return f"{{{type_name}}}-{'_'.join(map(str, key_values))}"

    def get_pattern(self, type_name: Text) -> Text:
        return f"{{{type_name}}}-*"
