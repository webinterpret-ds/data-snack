import pymongo
from dataclasses import dataclass
from pymongo import DeleteOne, UpdateOne
from typing import Optional, Dict, Type, List, Union, Any
from data_snack.entities import Entity

from data_snack.connections.base import Connection
from data_snack.key_factories import Key


def validate_keys(method):
    def method_wrapper(self, keys: Union[Dict[Key, Any], List[Key]]):
        if len(set([key.entity for key in keys])) > 1:
            # TODO: consider handling len(keys) == 0 in Snack or validate it here (seems to be worse)
            raise Exception(f"{method.__name__} is supported for one entity at the time for MongoDB.")
        return method(self, keys)
    return method_wrapper


@dataclass
class MongoConnection(Connection):
    connection: "pymongo.database.Database"

    def _get_entity_collection(self, entity_type: Type[Entity]) -> pymongo.collection.Collection:
        collection = self.connection[entity_type]
        collection.create_index(
            [(key, pymongo.ASCENDING) for key in entity_type.Meta.keys],
            unique=True
        )
        return collection

    def get(self, key: Key) -> Optional[bytes]:
        collection = self._get_entity_collection(key.entity)
        result = collection.find_one({"_id": key})
        if not result:
            return None
        del result['_id']
        return result  # TODO: wrong typing - investigate

    @validate_keys
    def get_many(self, keys: List[Key]) -> Dict[str, Optional[Dict]]:
        entity_type = keys[0].entity

        def _delete_id_field(result: Dict):
            if result:
                del result['_id']
            return result
        collection = self._get_entity_collection(entity_type)
        return {
            row["_id"]: _delete_id_field(row)
            for row in collection.find({"_id": {"$in": keys}})
        }

    def set(self, key: Key, value: Dict, expire: int = None) -> bool:
        collection = self._get_entity_collection(key.entity)
        try:
            collection.update_one({"_id": key}, {"$set": value}, upsert=True)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    def set_many(self, values: Dict[Key, str]) -> bool:
        # TODO: consider handling empty dicts in Snack
        entity_type = list(values.keys())[0].entity

        collection = self._get_entity_collection(entity_type)
        updates = [
            UpdateOne({"_id": key}, {"$set": value}, upsert=True)
            for key, value in values.items()
        ]
        result = collection.bulk_write(updates)
        set_count = result.inserted_count + result.upserted_count + max(result.modified_count, result.matched_count)
        return set_count == len(updates)

    def delete(self, key: Key) -> bool:
        collection = self._get_entity_collection(key.entity)
        result = collection.delete_one({"_id": key})
        return result.deleted_count == 1

    @validate_keys
    def delete_many(self, keys: List[Key]) -> bool:
        # TODO: move this validation to the decorator
        if len(set([key.entity for key in keys])) != 1:
            raise Exception("get_many is supported for one entity at the time for MongoDB.")
        entity_type = keys[0].entity

        collection = self._get_entity_collection(entity_type)
        updates = [DeleteOne({"_id": key}) for key in keys]
        result = collection.bulk_write(updates)
        return result.deleted_count == len(updates)

    def keys(self, pattern: str) -> List[str]:
        raise NotImplementedError()
