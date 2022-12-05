from abc import abstractmethod
from typing import Protocol, Text, List, Dict, Union, Any


class Connection(Protocol):
    """
    An interface used for by `Snack` to access db.
    If you want to create a custom connection to a db for your choosing,
    create a new class that follows this protocol.
    """
    connection: Any()

    @abstractmethod
    def get(self, key: Text) -> bytes:
        """
        Reads data from db based on provided key.

        :param key: unique data identifier
        :return: retrieved data
        """
        ...

    @abstractmethod
    def set(self, key: Text, value: Union[Text, bytes]) -> bool:
        """

        :param key: unique data identifier
        :param value: value saved in db
        :return: True if data was saved
        """
        ...

    @abstractmethod
    def get_many(self, keys: List[Text]) -> Dict[Text, bytes]:
        """

        :param keys:
        :return:
        """
        ...

    @abstractmethod
    def set_many(self, values: Dict[Text, Union[Text, bytes]]):
        """

        :param values:
        :return:
        """
        ...

    @abstractmethod
    def keys(self, pattern: Text) -> List[bytes]:
        """

        :param pattern:
        :return:
        """
        ...
