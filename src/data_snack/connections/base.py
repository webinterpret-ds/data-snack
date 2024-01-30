from typing import Any, Dict, List, Optional, Protocol

from data_snack.key_factories import Key


# TODO: consider converting Connection to an abstract class or remove inheritance in concrete connections
class Connection(Protocol):
    """
    An interface used for by `Snack` to access db.
    If you want to create a custom connection to a db for your choosing,
    create a new class that follows this protocol.
    """

    connection: Any

    def get(self, key: Key) -> Optional[Any]:
        """
        Reads data from db based on provided key.
        If key was missing in db, it returns None.

        :param key: unique data identifier
        :return: retrieved data
        """
        ...

    def get_many(self, keys: List[Key]) -> Dict[str, Optional[Any]]:
        """
        Reads multiple values from db based on provided list of keys.
        If a certain key was missing in db, it returns None for that value.

        :param keys: a list of keys
        :return: a dictionary with retrieved values assigned to each key
        """
        ...

    def set(self, key: Key, value: Any, expire: int = 0) -> bool:
        """
        Saves given value using provided key.

        :param key: unique data identifier
        :param value: value saved in db
        :param expire: number of seconds until the item is expired, or zero for no expiry
        :return: True if data was saved
        """
        ...

    def set_many(self, values: Dict[Key, Any]) -> Any:
        """
        Saves multiple values in db

        :param values: a dictionary containing keys and corresponding values
        :return: a list of keys successfully saved in db
        """
        ...

    def delete(self, key: Key) -> bool:
        """
        Deletes value for provided key.

        :param key: unique data identifier
        :return: True if data were deleted
        """
        ...

    def delete_many(self, keys: List[Key]) -> bool:
        """
        Deletes values for provided keys.

        :param keys: a list of keys
        :return: True if data were deleted
        """
        ...

    def keys(self, pattern: str) -> List[str]:
        """
        Retrieves keys from db that follows given pattern.

        :param pattern: pattern used to select only a subset of keys
        :return: a list of retrieved keys
        """
        ...
