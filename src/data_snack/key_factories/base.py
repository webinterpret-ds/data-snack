from typing import Protocol, Text, runtime_checkable


@runtime_checkable
class KeyFactory(Protocol):
    """
    An interface for key factories.
    Use it to create a new key factory.
    """

    def get_key(self, type_name: Text, *key_values: str) -> Text:
        """
        Gets key string.

        :param type_name: type name
        :param key_values: key values
        :return: key string in specified format
        """
        ...

    def get_pattern(self, type_name: Text, pattern: Text = "*") -> Text:
        """
        Gets pattern string.

        :param type_name: type name
        :param pattern: pattern to match
        :return: pattern string in specified format
        """
        ...
