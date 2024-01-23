import pymongo
from dataclasses import dataclass
from pymongo import DeleteOne, UpdateOne
from pymongo.database import Database
from typing import Optional, Dict, Type, List
from data_snack.entities import Entity

from data_snack.connections.base import Connection


@dataclass
class MongoConnection(Connection):
    connection: Database

    def _get_entity_collection(self, entity_type: Type[Entity]) -> pymongo.collection.Collection:
        collection = self.connection[entity_type.__name__]
        collection.create_index(
            [(key, pymongo.ASCENDING) for key in entity_type.Meta.keys],
            unique=True
        )
        return collection

    def get(self, entity_type: Type[Entity], key: str) -> Optional[bytes]:
        collection = self._get_entity_collection(entity_type)
        result = collection.find_one({"_id": key})
        if not result:
            return None
        del result['_id']
        return result

    def get_many(self, entity_type: Type[Entity], keys: List[str]) -> Dict[str, Optional[Dict]]:
        def _delete_id_field(result: Dict):
            if result:
                del result['_id']
            return result

        collection = self._get_entity_collection(entity_type)
        return {
            row["_id"]: _delete_id_field(row)
            for row in collection.find({"_id": {"$in": keys}})
        }


    def set(self, entity_type: Type[Entity], key: str, value: Dict, expire: int = None) -> bool:
        collection = self._get_entity_collection(entity_type)
        try:
            collection.update_one({ "_id": key }, {"$set": value}, upsert=True)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    def set_many(self, entity_type: Type[Entity], values: Dict[str, str]) -> List[str]:
        collection = self._get_entity_collection(entity_type)
        updates = [
            UpdateOne({"_id": key}, {"$set": value}, upsert=True)
            for key, value in values.items()
        ]
        result = collection.bulk_write(updates)
        set_count = result.inserted_count + result.upserted_count + max(result.modified_count, result.matched_count)
        return set_count == len(updates)

    def delete(self, entity_type: Type[Entity], key: Dict) -> bool:
        collection = self._get_entity_collection(entity_type)
        result = collection.delete_one({"_id": key})
        return result.deleted_count == 1

    def delete_many(self, entity_type: Type[Entity], keys: List[str]) -> bool:
        collection = self._get_entity_collection(entity_type)
        updates = [DeleteOne({"_id": key}) for key in keys]
        result = collection.bulk_write(updates)
        return result.deleted_count == len(updates)

    def keys(self, pattern: str) -> List[str]:
        raise NotImplementedError()
