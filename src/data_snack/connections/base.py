from typing import Any, Dict, List, Protocol, Text, Union


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

    def set(self, key: Text, value: Union[Text, bytes], expire: int = 0) -> bool:
        """
        Saves given value using provided key.

        :param key: unique data identifier
        :param value: value saved in db
        :param expire: number of seconds until the item is expired, or zero for no expiry
        :return: True if data was saved
        """
        ...

    def delete(self, key: Text) -> bool:
        """
        Deletes value for provided key.

        :param key: unique data identifier
        :return: True if data were deleted
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
        :return: a list of keys successfully saved in db
        """
        ...

    def delete_many(self, keys: List[Text]) -> bool:
        """
        Deletes values for provided keys.

        :param keys: a list of keys
        :return: True if data were deleted
        """
        ...

    def keys(self, pattern: Text) -> List[Text]:
        """
        Retrieves keys from db that follows given pattern.

        :param pattern: pattern used to select only a subset of keys
        :return: a list of retrieved keys
        """
        ...
