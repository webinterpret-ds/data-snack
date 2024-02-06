from dataclasses import dataclass
from typing import Dict, Optional, List
from unittest import TestCase
from unittest.mock import Mock

import pymongo.errors
from parameterized import parameterized
from pymongo import UpdateOne

from data_snack.entities import Entity
from data_snack.key_factories import NonClusterKey
from tests.data_snack.conftest import Car
from data_snack.connections.mongo import MongoConnection


class TestMongoConnection(TestCase):

    def setUp(self) -> None:
        self.key_factory = NonClusterKey
        self.entity_type = Car
        self.collection = Mock()
        self.mongo_db = {"Car": self.collection}
        self.mongo_connection = MongoConnection(connection=self.mongo_db)

    def test_get_record_found_expect_returned_without_id_field(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=["1"])

        def find_one(query: Dict[str, str]) -> Optional[Dict]:
            if query == {"_id": "Car-1"}:
                return {"_id": "Car-1", "index": "1", "brand": "BMW"}

        self.collection.find_one = find_one
        expected = {"index": "1", "brand": "BMW"}

        # act
        result = self.mongo_connection.get(key)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    def test_get_record_not_found_expect_none_returned(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        self.collection.find_one.return_value = None

        # act
        result = self.mongo_connection.get(key)

        # assert
        self.assertIsNone(result)
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    def test_get_many_all_records_found_expect_returned_all_in_desired_format(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=["2"])
        keys = [key1, key2]

        def find(query: Dict) -> Optional[List[Dict]]:
            if query == {"_id": {"$in": ["Car-1", "Car-2"]}}:
                return [
                    {"_id": "Car-1", "index": "1", "brand": "BMW"},
                    {"_id": "Car-2", "index": "2", "brand": "VW"}
                ]
        self.collection.find = find
        expected = {
            "Car-1": {"index": "1", "brand": "BMW"},
            "Car-2": {"index": "2", "brand": "VW"},
        }

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    def test_get_many_not_all_records_found_expect_returned_found_in_desired_format(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=["2"])
        keys = [key1, key2]

        def find(query: Dict) -> Optional[List[Dict]]:
            if query == {"_id": {"$in": ["Car-1", "Car-2"]}}:
                return [
                    {"_id": "Car-2", "index": "2", "brand": "VW"}
                ]
        self.collection.find = find
        expected = {"Car-2": {"index": "2", "brand": "VW"}}

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    def test_get_many_no_records_found_expect_empty_dict_returned(self) -> None:
        # arrange
        key1 = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=["2"])
        keys = [key1, key2]

        def find(query: Dict) -> Optional[List]:
            if query == {"_id": {"$in": ["Car-1", "Car-2"]}}:
                return []
        self.collection.find = find
        expected = {}

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    def test_get_many_empty_list_of_keys_passed_expect_empty_dict_returned(self) -> None:
        # arrange
        keys = []
        expected = {}

        # act
        result = self.mongo_connection.get_many(keys)

        # assert
        self.assertEqual(result, expected)

    def test_get_many_many_entity_types_expect_value_error_raised(self) -> None:
        # arrange
        @dataclass
        class DummyEntity(Entity):
            field: str

            class Meta:
                keys = ["field"]
                excluded_fields = []

        key1 = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        key2 = self.key_factory(entity_type=DummyEntity, key_values=[1])
        keys = [key1, key2]

        # act & assert
        with self.assertRaises(ValueError):
            self.mongo_connection.get_many(keys)

    def test_set_successful_expect_true_returned(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        value = {"index": "1", "brand": "BMW"}

        # act
        result = self.mongo_connection.set(key=key, value=value)

        # assert
        self.collection.update_one.assert_called_once_with({"_id": "Car-1"}, {"$set": value}, upsert=True)
        self.assertTrue(result)
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    def test_set_raised_duplicate_key_error_expect_false_returned(self) -> None:
        # arrange
        key = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        value = {"index": "1", "brand": "BMW"}
        self.collection.update_one.side_effect = pymongo.errors.DuplicateKeyError(error="dummy")

        # act
        result = self.mongo_connection.set(key=key, value=value)

        # assert
        self.collection.update_one.assert_called_once_with({"_id": "Car-1"}, {"$set": value}, upsert=True)
        self.assertFalse(result)
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    @parameterized.expand(
        [
            ("only inserts", 3, 0, 0, 0, True),
            ("only upserts", 0, 3, 0, 0, True),
            ("only modified", 0, 0, 3, 0, True),
            ("only matched", 0, 0, 0, 3, True),
            ("two inserts one upsert", 2, 1, 0, 0, True),
            ("two inserts one modified", 2, 0, 1, 0, True),
            ("two inserts one matched", 2, 0, 0, 1, True),
            ("two inserts one upsert one matched", 2, 0, 1, 1, True),  # hypothetical scenario
            ("two upserts one insert", 1, 2, 0, 0, True),
            ("two upserts one modified", 0, 2, 1, 0, True),
            ("two upserts one matched", 0, 2, 0, 1, True),
            ("two upserts one modified one matched", 0, 2, 1, 1, True),  # hypothetical scenario
            ("three modified one updated", 0, 0, 3, 1, True),  # hypothetical scenario
            ("three updated one modified", 0, 0, 1, 3, True),  # hypothetical scenario
            ("one insert one upsert one modified", 1, 1, 1, 0, True),
            ("one insert one upsert one matched", 1, 1, 0, 1, True),
            ("one insert one upsert one modified one modified", 1, 1, 1, 1, True),  # hypothetical scenario
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
        key1 = self.key_factory(entity_type=self.entity_type, key_values=["1"])
        key2 = self.key_factory(entity_type=self.entity_type, key_values=["2"])
        key3 = self.key_factory(entity_type=self.entity_type, key_values=["3"])
        value1 = {"index": "1", "brand": "BMW"}
        value2 = {"index": "2", "brand": "VW"}
        value3 = {"index": "3", "brand": "Audi"}
        updates = [
            UpdateOne({"_id": "Car-1"}, {"$set": value1}, upsert=True),
            UpdateOne({"_id": "Car-2"}, {"$set": value2}, upsert=True),
            UpdateOne({"_id": "Car-3"}, {"$set": value3}, upsert=True),
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
        self.collection.create_index.assert_called_once_with([("index", 1)], unique=True)

    def test_entity_with_many_key_fields_expect_indices_created_for_all_of_them(self) -> None:
        ...
