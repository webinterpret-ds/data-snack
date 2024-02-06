from dataclasses import dataclass
from typing import Dict, Optional, List
from unittest import TestCase
from unittest.mock import Mock

import pymongo.errors
from parameterized import parameterized
from pymongo import UpdateOne, DeleteOne

from data_snack.connections.mongo import MongoConnection
from data_snack.entities import Entity
from data_snack.key_factories import NonClusterKey


class TestMongoConnection(TestCase):

    def setUp(self) -> None:
        @dataclass
        class ManyKeysEntity(Entity):
            key1: int
            key2: int

            class Meta:
                keys = ["key1", "key2"]
                excluded_fields = []

        @dataclass
        class DummyEntity(Entity):
            field: int

            class Meta:
                keys = ["field"]
                excluded_fields = []

        self.key_factory = NonClusterKey
        self.entity_type = ManyKeysEntity
        self.dummy_entity_type = DummyEntity
        self.collection = Mock()
        self.mongo_db = {"ManyKeysEntity": self.collection, DummyEntity: self.collection}
        self.mongo_connection = MongoConnection(connection=self.mongo_db)

    def test_get_record_found_expect_returned_without_id_field(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])

        def find_one(query: Dict[str, str]) -> Optional[Dict]:
            if query == {"_id": "ManyKeysEntity-1_1"}:
                return {"_id": "ManyKeysEntity-1_1", "key1": "1", "key2": "1"}

        self.collection.find_one = find_one
        expected = {"key1": "1", "key2": "1"}

        # act
        result = self.mongo_connection.get(key)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_get_record_not_found_expect_none_returned(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        self.collection.find_one.return_value = None

        # act
        result = self.mongo_connection.get(key)

        # assert
        self.assertIsNone(result)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_get_many_all_records_found_expect_returned_all_in_desired_format(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=[2, 2])
        keys = [key1, key2]

        def find(query: Dict) -> Optional[List[Dict]]:
            if query == {"_id": {"$in": ["ManyKeysEntity-1_1", "ManyKeysEntity-2_2"]}}:
                return [
                    {"_id": "ManyKeysEntity-1_1", "key1": "1", "key2": "1"},
                    {"_id": "ManyKeysEntity-2_2", "key1": "2", "key2": "2"}
                ]
        self.collection.find = find
        expected = {
            "ManyKeysEntity-1_1": {"key1": "1", "key2": "1"},
            "ManyKeysEntity-2_2": {"key1": "2", "key2": "2"},
        }

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_get_many_not_all_records_found_expect_returned_found_in_desired_format(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=[2, 2])
        keys = [key1, key2]

        def find(query: Dict) -> Optional[List[Dict]]:
            if query == {"_id": {"$in": ["ManyKeysEntity-1_1", "ManyKeysEntity-2_2"]}}:
                return [
                    {"_id": "ManyKeysEntity-2_2", "key1": "2", "key2": "2"}
                ]
        self.collection.find = find
        expected = {"ManyKeysEntity-2_2": {"key1": "2", "key2": "2"}}

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_get_many_no_records_found_expect_empty_dict_returned(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=[2, 2])
        keys = [key1, key2]

        def find(query: Dict) -> Optional[List]:
            if query == {"_id": {"$in": ["ManyKeysEntity-1_1", "ManyKeysEntity-2_2"]}}:
                return []
        self.collection.find = find
        expected = {}

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_get_many_empty_list_of_keys_passed_expect_empty_dict_returned(self) -> None:
        # arrange
        keys = []
        expected = {}

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_not_called()
        self.collection.find.assert_not_called()

    def test_get_many_many_entity_types_expect_value_error_raised(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(entity_type=self.dummy_entity_type, key_values=[1])
        keys = [key1, key2]

        # act & assert
        with self.assertRaises(ValueError):
            self.mongo_connection.get_many(keys)

        self.collection.create_index.assert_not_called()
        self.collection.find.assert_not_called()

    def test_set_successful_expect_true_returned(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        value = {"key1": "1", "key2": "2"}

        # act
        result = self.mongo_connection.set(key=key, value=value)

        # assert
        self.collection.update_one.assert_called_once_with({"_id": "ManyKeysEntity-1_1"}, {"$set": value}, upsert=True)
        self.assertTrue(result)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_set_raised_duplicate_key_error_expect_false_returned(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        value = {"key1": "1", "key2": "2"}
        self.collection.update_one.side_effect = pymongo.errors.DuplicateKeyError(error="dummy")

        # act
        result = self.mongo_connection.set(key=key, value=value)

        # assert
        self.collection.update_one.assert_called_once_with({"_id": "ManyKeysEntity-1_1"}, {"$set": value}, upsert=True)
        self.assertFalse(result)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    @parameterized.expand(
        [
            ("only inserts", 3, 0, 0, 0, True),
            ("only upserts", 0, 3, 0, 0, True),
            ("only modified", 0, 0, 3, 0, True),
            ("only matched", 0, 0, 0, 3, True),
            ("two inserts one upsert", 2, 1, 0, 0, True),
            ("two inserts one modified", 2, 0, 1, 0, True),
            ("two inserts one matched", 2, 0, 0, 1, True),
            ("two upserts one insert", 1, 2, 0, 0, True),
            ("two upserts one modified", 0, 2, 1, 0, True),
            ("two upserts one matched", 0, 2, 0, 1, True),
            ("one insert one upsert one modified", 1, 1, 1, 0, True),
            ("one insert one upsert one matched", 1, 1, 0, 1, True),
            ("one insert one modified one matched", 1, 0, 1, 1, False),
            ("one upsert one modified one matched", 0, 1, 1, 1, False),
        ]
    )
    def test_set_many_successful_expect_desired_bool(
        self,
        name: str,
        inserted_count: int,
        upserted_count: int,
        modified_count: int,
        matched_count: int,
        desired_bool: bool,
    ) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=[2, 2])
        key3 = self.key_factory(entity_type=self.entity_type, key_values=[3, 3])
        value1 = {"key1": "1", "key2": "1"}
        value2 = {"key1": "2", "key2": "2"}
        value3 = {"key1": "3", "key2": "3"}
        updates = [
            UpdateOne({"_id": "ManyKeysEntity-1_1"}, {"$set": value1}, upsert=True),
            UpdateOne({"_id": "ManyKeysEntity-2_2"}, {"$set": value2}, upsert=True),
            UpdateOne({"_id": "ManyKeysEntity-3_3"}, {"$set": value3}, upsert=True),
        ]
        values = {key1: value1, key2: value2, key3: value3}
        self.collection.bulk_write.return_value = Mock(
            inserted_count=inserted_count,
            upserted_count=upserted_count,
            modified_count=modified_count,
            matched_count=matched_count,
        )

        # act
        result = self.mongo_connection.set_many(values)

        # assert
        self.collection.bulk_write.assert_called_once_with(updates)
        self.assertEqual(result, desired_bool)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_set_many_empty_dict_of_values_passed_expect_true_returned(self) -> None:
        # arrange
        values = {}

        # act
        result = self.mongo_connection.set_many(values)

        # assert
        self.collection.bulk_write.assert_not_called()
        self.assertTrue(result)
        self.collection.create_index.assert_not_called()

    def test_set_many_many_entity_types_expect_value_error_raised(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(entity_type=self.dummy_entity_type, key_values=[1])
        value1 = {"key1": "1", "key2": "1"}
        value2 = {"field": 1}
        values = {key1: value1, key2: value2}

        # act & assert
        with self.assertRaises(ValueError):
            self.mongo_connection.set_many(values)

        self.collection.bulk_write.assert_not_called()
        self.collection.create_index.assert_not_called()

    @parameterized.expand([("successful", 1, True), ("unsuccessful", 0, False)])
    def test_delete_expect_desired_bool(self, name: str, n_deleted: int, desired_bool: bool) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])

        def delete_one(query: Dict[str, str]) -> int:
            if query == {"_id": "ManyKeysEntity-1_1"}:
                return Mock(deleted_count=n_deleted)

        self.collection.delete_one = delete_one

        # act
        result = self.mongo_connection.delete(key)

        # assert
        self.assertEqual(result, desired_bool)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    @parameterized.expand([("all deleted", 2, True), ("not all deleted", 1, False)])
    def test_delete_many_successful_expect_desired_bool(self, name: str, n_deleted: int, desired_bool: bool) -> None:
        # arrange
        key1 = self.key_factory(self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(self.entity_type, key_values=[2, 2])
        keys = [key1, key2]
        updates = [DeleteOne({"_id": "ManyKeysEntity-1_1"}), DeleteOne({"_id": "ManyKeysEntity-2_2"})]
        self.collection.bulk_write.return_value = Mock(deleted_count=n_deleted)

        # act
        result = self.mongo_connection.delete_many(keys)

        # assert
        self.collection.bulk_write.assert_called_once_with(updates)
        self.assertEqual(result, desired_bool)
        self.collection.create_index.assert_called_once_with(
            [("key1", pymongo.ASCENDING), ("key2", pymongo.ASCENDING)], unique=True
        )

    def test_delete_many_empty_list_of_keys_passed_expect_true_returned(self) -> None:
        # arrange
        keys = []

        # act
        result = self.mongo_connection.delete_many(keys)

        # assert
        self.collection.bulk_write.assert_not_called()
        self.assertTrue(result)
        self.collection.create_index.assert_not_called()

    def test_delete_many_many_entity_types_expect_value_error_raised(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=[1, 1])
        key2 = self.key_factory(entity_type=self.dummy_entity_type, key_values=[1])
        keys = [key1, key2]

        # act & assert
        with self.assertRaises(ValueError):
            self.mongo_connection.delete_many(keys)

        self.collection.bulk_write.assert_not_called()
        self.collection.create_index.assert_not_called()

    def test_keys_expect_raise_not_implemented_error(self) -> None:
        # act & assert
        with self.assertRaises(NotImplementedError):
            self.mongo_connection.keys(pattern="dummy")
