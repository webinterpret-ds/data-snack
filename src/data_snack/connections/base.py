from abc import abstractmethod
from typing import Protocol, Text, List, Dict, Union, Any


class Connection(Protocol):
    """
    An interface used for by `Snack` to access db.
    If you want to create a custom connection to a db for your choosing,
    create a new class that follows this protocol.
    """
    connection: Any

    def get(self, key: Text) -> bytes:
        """
        Reads data from db based on provided key.

        :param key: unique data identifier
        :return: retrieved data
        """
        ...

    def set(self, key: Text, value: Union[Text, bytes]) -> bool:
        """
        Saves given value using provided key.

        :param key: unique data identifier
        :param value: value saved in db
        :return: True if data was saved
        """
        ...

    def get_many(self, keys: List[Text]) -> Dict[Text, bytes]:
        """
        Reads multiple values from db based on provided list of keys.

        :param keys: a list of keys
        :return: a dictionary with retrieved values assigned to each key
        """
        ...

    def set_many(self, values: Dict[Text, Union[Text, bytes]]) -> List[Text]:
        """
        Saves multiple values in db

        :param values: a dictionary containing keys and corresponding values
        :return: a list of keys succesfully saved in db
        """
        ...

    def keys(self, pattern: Text) -> List[Text]:
        """
        Retrieves keys from db that follows given pattern.

        :param pattern: pattern used to select only a subset of keys
        :return: a list of retrieved keys
        """
        ...
