from unittest.mock import MagicMock, Mock

import pytest

from data_snack.connections.memcached import MemcachedConnection


@pytest.fixture
def connection() -> MemcachedConnection:
    """A `MemcachedConnection` with mocked connection to the actual database."""
    return MemcachedConnection(connection=MagicMock())


def test_get(connection: MemcachedConnection) -> None:
    """Testing getting a single value based of the provided key."""
    connection.connection.get.return_value = "value"
    key = Mock()

    result = connection.get(key)
    assert result == "value"
    connection.connection.get.assert_called_with(key.keystring)


def test_set(connection: MemcachedConnection) -> None:
    """Testing setting a single value based for the provided key."""
    key = Mock()
    connection.connection.set.return_value = key

    result = connection.set(key, "value")
    assert result == key
    connection.connection.set.assert_called_with(key.keystring, "value", expire=0)


def test_set_expire(connection: MemcachedConnection) -> None:
    """Testing setting a single value based for the provided key."""
    key = Mock()
    connection.connection.set.return_value = key

    result = connection.set(key, "value", 100)
    assert result == key
    connection.connection.set.assert_called_with(key.keystring, "value", expire=100)


def test_delete(connection: MemcachedConnection) -> None:
    """Testing deleting a single value based of the provided key."""
    connection.connection.delete.return_value = True
    key = Mock()

    result = connection.delete(key)
    assert result
    connection.connection.delete.assert_called_with(key.keystring, noreply=False)


def test_get_many(connection: MemcachedConnection) -> None:
    """Testing getting multiple values based on a provided list of keys."""
    key1, key2 = Mock(), Mock()
    connection.connection.get_many.return_value = {key1: "value1", key2: "value2"}

    result = connection.get_many([key1, key2])
    assert result == {key1: "value1", key2: "value2"}
    connection.connection.get_many.assert_called_with([key1.keystring, key2.keystring])


def test_set_many(connection: MemcachedConnection) -> None:
    """Testing setting multiple values. Values are provided in a form of a dictionary."""
    key1, key2 = Mock(), Mock()
    connection.connection.set_many.return_value = []
    set_mapping = {key1: "value1", key2: "value2"}

    result = connection.set_many(set_mapping)
    assert result == [key1, key2]
    connection.connection.set_many.assert_called_with({key1.keystring: "value1", key2.keystring: "value2"})


def test_set_many_failed_one_key(connection: MemcachedConnection) -> None:
    """Testing setting multiple values when one key failed. Values are provided in a form of a dictionary."""
    key1, key2 = Mock(), Mock()
    connection.connection.set_many.return_value = [key1.keystring]
    set_mapping = {key1: "value1", key2: "value2"}

    result = connection.set_many(set_mapping)
    assert result == [key2]
    connection.connection.set_many.assert_called_with({key1.keystring: "value1", key2.keystring: "value2"})


def test_delete_many(connection: MemcachedConnection) -> None:
    """Testing deleting multiple values based on a provided list of keys."""
    connection.connection.delete_many.return_value = True
    key1, key2 = Mock(), Mock()

    result = connection.delete_many([key1, key2])
    assert result
    connection.connection.delete_many.assert_called_with(
        [key1.keystring, key2.keystring], noreply=False
    )


def test_keys(connection: MemcachedConnection) -> None:
    """Testing getting a list of keys based on a provided text query."""
    with pytest.raises(NotImplementedError):
        connection.keys("*")
