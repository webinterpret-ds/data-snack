from typing import Protocol, Text


class KeyFactory(Protocol):
    """
    An interface for key factories.
    Use it to create a new key factory.
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
