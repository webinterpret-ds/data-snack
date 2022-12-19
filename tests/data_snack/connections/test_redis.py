from unittest.mock import MagicMock

import pytest

from data_snack.connections.redis import RedisConnection


@pytest.fixture
def connection() -> RedisConnection:
    """A `RedisConnection` with mocked connection to the actual database."""
    return RedisConnection(connection=MagicMock())


def test_get(connection: RedisConnection) -> None:
    """Testing getting a single value based of the provided key."""
    connection.connection.get.return_value = "value"

    result = connection.get("key")
    assert result == "value"
    connection.connection.get.assert_called_with("key")


def test_set(connection: RedisConnection) -> None:
    """Testing setting a single value based for the provided key."""
    connection.connection.set.return_value = "key"

    result = connection.set("key", "value", 100)
    assert result == "key"
    connection.connection.set.assert_called_with("key", "value", ex=100)


def test_delete(connection: RedisConnection) -> None:
    """Testing deleting a single value based of the provided key."""
    connection.connection.delete.return_value = 1

    result = connection.delete("key")
    assert result
    connection.connection.delete.assert_called_with("key")


def test_get_many(connection: RedisConnection) -> None:
    """Testing getting multiple values based on a provided list of keys."""
    connection.connection.mget.return_value = ["value1", "value2"]

    result = connection.get_many(["key1", "key2"])
    assert result == {"key1": "value1", "key2": "value2"}
    connection.connection.mget.assert_called_with(["key1", "key2"])


def test_set_many(connection: RedisConnection) -> None:
    """Testing setting multiple values. Values are provided in a form of a dictionary."""
    connection.connection.set.side_effect = ["key1", "key2"]
    set_mapping = {"key1": "value1", "key2": "value2"}

    result = connection.set_many(set_mapping, 100)
    assert set(result) == {"key1", "key2"}
    for k, v in set_mapping:
        connection.connection.set.assert_called_with(k, v, ex=100)


def test_delete_many(connection: RedisConnection) -> None:
    """Testing deleting multiple values based on a provided list of keys."""
    connection.connection.delete.return_value = 2

    result = connection.delete_many(["key1", "key2"])
    assert result
    connection.connection.delete.assert_called_with(*["key1", "key2"])


def test_keys(connection: RedisConnection) -> None:
    """Testing getting a list of keys based on a provided text query."""
    connection.connection.keys.return_value = ["key"]

    result = connection.keys("*")
    assert result == ["key"]
