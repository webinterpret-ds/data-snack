from dataclasses import dataclass, field
from typing import Text, Dict, List, Optional

from .connections import Connection
from .entities import EntityRegistry, EntityType, Entity
from .exceptions import EntityAlreadyRegistered, WrongKeyValue
from .serializers import Serializer, DataclassSerializer


def _build_key(type_name: Text, *keys: Text):
    return f"{type_name}-{'_'.join(keys)}"


@dataclass
class Snack:
    connection: Connection
    registry: Dict[Text, EntityRegistry] = field(default_factory=dict)

    def register_entity(self, cls: EntityType, keys: List[Text], serializer: Serializer = None):
        type_name = cls.__name__

        if type_name in self.registry:
            raise EntityAlreadyRegistered(f"Entity {type_name} is already registred")

        if not keys:
            raise WrongKeyValue("Entity keys cannot be empty")

        for key in keys:
            if key not in cls.__dataclass_fields__.keys():
                raise WrongKeyValue(f"Key {key} not found in entity definition.")

        if not serializer:
            serializer = DataclassSerializer(cls)

        self.registry[type_name] = EntityRegistry(
            entity=cls,
            serializer=serializer,
            keys=keys
        )

    def create_wrap(self, cls: EntityType) -> "EntityWrap":
        return EntityWrap(self, cls)

    def _get_serializer(self, type_name: Text) -> Serializer:
        return self.registry[type_name].serializer

    def _build_record_key(self, type_name: Text, entity: Entity) -> Text:
        key_values = [
            getattr(entity, key)
            for key in self.registry[type_name].keys
        ]
        return _build_key(type_name, *key_values)

    def set(self, entity: Entity) -> Optional[Text]:
        type_name = entity.__class__.__name__
        key = self._build_record_key(type_name, entity)
        record = self._get_serializer(type_name).serialize(entity)
        if self.connection.set(key, record):
            return key

    def get(self, cls: EntityType, key: List[Text]) -> Entity:
        type_name = cls.__name__
        _key = _build_key(type_name, *key)
        if value := self.connection.get(_key):
            return self._get_serializer(type_name).deserialize(value)
        else:
            raise KeyError(f"Key {_key} not found.")

    def get_many(self, cls: EntityType, keys: List[List[Text]]) -> List[Entity]:
        type_name = cls.__name__
        _keys = [_build_key(type_name, *key) for key in keys]
        records = self.connection.get_many(_keys).values()
        return self._get_serializer(type_name).deserialize(records, many=True)

    def set_many(self, entities: List[Entity]) -> List[Text]:
        type_name = entities[0].__class__.__name__
        records = self._get_serializer(type_name).serialize(entities, many=True)
        keys = [
            self._build_record_key(type_name, entity)
            for entity in entities
        ]
        if result := self.connection.set_many(dict(zip(keys, records))):
            return result

    def keys(self, cls: EntityType) -> List[bytes]:
        return self.connection.keys(pattern=f'{cls.__name__}-*')


@dataclass
class EntityWrap:
    snack: Snack
    entity_type: EntityType
    _entity_type_name: Text = field(init=False)

    @property
    def entity_type_name(self) -> Text:
        return self._entity_type_name

    def __post_init__(self):
        self._entity_type_name = self.entity_type.__name__

    def set(self, entity: Entity) -> Optional[Text]:
        return self.snack.set(entity)

    def get(self, key: List[Text]) -> Entity:
        return self.snack.get(self.entity_type, key)

    def get_many(self, keys: List[List[Text]]) -> List[Entity]:
        return self.snack.get_many(self.entity_type, keys)

    def set_many(self, entities: List[Entity]) -> List[Text]:
        return self.snack.set_many(entities)

    def keys(self) -> List[bytes]:
        return self.snack.keys(self.entity_type)
