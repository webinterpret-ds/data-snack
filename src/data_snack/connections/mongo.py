from dataclasses import dataclass
from typing import Optional, Dict, Type, List, Union, Any

import pymongo
from pymongo import DeleteOne, UpdateOne

from data_snack.connections.base import Connection
from data_snack.entities import Entity
from data_snack.key_factories import Key
from data_snack.utils import get_attribute_of_first_element_from_iterable


def validate_keys(method):
    def method_wrapper(self, keys: Union[Dict[Key, Any], List[Key]], /):
        if len(set([key.entity_type for key in keys])) > 1:
            raise ValueError(f"{method.__name__} is supported for one entity at the time for MongoDB.")
        return method(self, keys)
    return method_wrapper


@dataclass
class MongoConnection(Connection):
    connection: "pymongo.database.Database"

    def _get_entity_collection(self, entity_type: Type[Entity]) -> pymongo.collection.Collection:
        collection = self.connection[entity_type.__name__]
        collection.create_index(
            [(key, pymongo.ASCENDING) for key in entity_type.Meta.keys],
            unique=True
        )
        return collection

    def get(self, key: Key) -> Optional[Dict]:
        collection = self._get_entity_collection(key.entity_type)
        result = collection.find_one({"_id": key.keystring})
        if not result:
            return None
        del result['_id']
        return result  # TODO: wrong typing - investigate

    @validate_keys
    def get_many(self, keys: List[Key], /) -> Dict[str, Optional[Dict]]:
        if not (entity_type := get_attribute_of_first_element_from_iterable(keys, "entity_type")):
            return {}
        db_keys = [key.keystring for key in keys]

        def _delete_id_field(result: Dict) -> Dict:
            if result:
                del result['_id']
            return result
        collection = self._get_entity_collection(entity_type)
        return {
            row["_id"]: _delete_id_field(row)
            for row in collection.find({"_id": {"$in": db_keys}})
        }

    def set(self, key: Key, value: Dict, **kwargs: Any) -> bool:
        collection = self._get_entity_collection(key.entity_type)
        try:
            collection.update_one({"_id": key.keystring}, {"$set": value}, upsert=True)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    @validate_keys
    def set_many(self, values: Dict[Key, Any], /) -> bool:
        if not (entity_type := get_attribute_of_first_element_from_iterable(values, "entity_type")):
            return True
        updates = [
            UpdateOne({"_id": key.keystring}, {"$set": value}, upsert=True)
            for key, value in values.items()
        ]
        collection = self._get_entity_collection(entity_type)
        result = collection.bulk_write(updates)
        set_count = result.inserted_count + result.upserted_count + max(result.modified_count, result.matched_count)
        return set_count == len(updates)

    def delete(self, key: Key) -> bool:
        collection = self._get_entity_collection(key.entity_type)
        result = collection.delete_one({"_id": key.keystring})
        return result.deleted_count == 1

    @validate_keys
    def delete_many(self, keys: List[Key], /) -> bool:
        if not (entity_type := get_attribute_of_first_element_from_iterable(keys, "entity_type")):
            return True

        collection = self._get_entity_collection(entity_type)
        updates = [DeleteOne({"_id": key.keystring}) for key in keys]
        result = collection.bulk_write(updates)
        return result.deleted_count == len(updates)

    def keys(self, pattern: str) -> List[str]:
        raise NotImplementedError()
