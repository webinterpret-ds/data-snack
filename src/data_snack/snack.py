import json
from dataclasses import dataclass, field
from typing import Text, Dict, List, Optional

from marshmallow.schema import SchemaMeta
from marshmallow_dataclass import class_schema

from .connection import Connection
from .entities import EntityRegistry, EntityType, Entity
from .exceptions import EntityAlreadyRegistered, WrongKeyValue


def _build_key(type_name: Text, *keys: Text):
    return f"{type_name}-{'_'.join(keys)}"


@dataclass
class Snack:
    connection: Connection
    registry: Dict[Text, EntityRegistry] = field(default_factory=dict)

    def register_entity(self, cls: EntityType, keys: List[Text], schema: SchemaMeta = None):
        type_name = cls.__name__

        if type_name in self.registry:
            raise EntityAlreadyRegistered(f"Entity {type_name} is already registred")

        if not keys:
            raise WrongKeyValue("Entity keys cannot be empty")

        for key in keys:
            if key not in cls.__dataclass_fields__.keys():
                raise WrongKeyValue(f"Key {key} not found in entity definition.")

        if not schema:
            schema = class_schema(cls)()

        self.registry[type_name] = EntityRegistry(
            entity=cls,
            schema=schema,
            keys=keys
        )

    def _get_schema(self, type_name: Text) -> SchemaMeta:
        return self.registry[type_name].schema

    def _build_record_key(self, type_name: Text, record: Dict) -> Text:
        key_values = [
            record[key]
            for key in self.registry[type_name].keys
        ]
        return _build_key(type_name, *key_values)

    def set(self, entity: Entity) -> Optional[Text]:
        type_name = entity.__class__.__name__
        record = self._get_schema(type_name).dump(entity)
        key = self._build_record_key(type_name, record)
        if self.connection.set(key, json.dumps(record)):
            return key

    def get(self, cls: EntityType, key: List[Text]) -> Entity:
        type_name = cls.__name__
        _key = _build_key(type_name, *key)
        record = json.loads(self.connection.get(_key).decode('utf-8'))
        return self._get_schema(type_name).load(record)

    def mget(self, cls: EntityType, keys: List[List[Text]]) -> List[Entity]:
        type_name = cls.__name__
        _keys = [_build_key(type_name, *key) for key in keys]
        records = [
            json.loads(brecord.decode('utf-8'))
            for brecord in self.connection.mget(_keys)
        ]
        return self._get_schema(type_name).load(records, many=True)

    def mset(self, entities: List[Entity]) -> List[Text]:
        type_name = entities[0].__class__.__name__
        records = self._get_schema(type_name).dump(entities, many=True)
        keys = [
            self._build_record_key(type_name, record)
            for record in records
        ]
        _records = [json.dumps(record) for record in records]
        if self.connection.mset(dict(zip(keys, _records))):
            return keys
