from dataclasses import dataclass, field
from typing import Text, Dict, List, Optional, Type

from .wrap import EntityWrap
from .connections import Connection
from .entities import EntityRegistry, Entity
from .exceptions import EntityAlreadyRegistered, WrongKeyValue
from .serializers import Serializer, DataclassSerializer


def _build_key(type_name: Text, *keys: Text):
    return f"{type_name}-{'_'.join(keys)}"


@dataclass
class Snack:
    """
    A core interface
    """

    connection: Connection
    registry: Dict[Text, EntityRegistry] = field(default_factory=dict)

    def register_entity(self, cls: Type[Entity], keys: List[Text], serializer: Serializer = None):
        """

        :param cls:
        :param keys:
        :param serializer:
        :return:
        """
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
            entity_type=cls,
            serializer=serializer,
            keys=keys
        )

    def create_wrap(self, cls: Type[Entity], wrap_type: Type["Wrap"] = EntityWrap) -> "Wrap":
        """

        :param cls:
        :param wrap_type:
        :return:
        """
        return wrap_type(self, cls)

    def _get_serializer(self, type_name: Text) -> Serializer:
        return self.registry[type_name].serializer

    def _build_record_key(self, type_name: Text, entity: Entity) -> Text:
        key_values = [
            getattr(entity, key)
            for key in self.registry[type_name].keys
        ]
        return _build_key(type_name, *key_values)

    def set(self, entity: Entity) -> Optional[Text]:
        """
        notice the entity stored in the db will be overwritten.
        make sure all the combined keys are unique for each entity

        :param entity:
        :return:
        """
        type_name = entity.__class__.__name__
        key = self._build_record_key(type_name, entity)
        record = self._get_serializer(type_name).serialize(entity)
        if self.connection.set(key, record):
            return key

    def get(self, cls: Type[Entity], key: List[Text]) -> Entity:
        """
        reads ane entity of `cls` type from db based on provided key

        :param cls:
        :param key:
        :return:
        """
        type_name = cls.__name__
        _key = _build_key(type_name, *key)
        if value := self.connection.get(_key):
            return self._get_serializer(type_name).deserialize(value)
        else:
            raise KeyError(f"Key {_key} not found.")

    def get_many(self, cls: Type[Entity], keys: List[List[Text]]) -> List[Entity]:
        """

        :param cls:
        :param keys:
        :return:
        """
        type_name = cls.__name__
        _keys = [_build_key(type_name, *key) for key in keys]
        records = list(self.connection.get_many(_keys).values())
        return self._get_serializer(type_name).deserialize(records, many=True)

    def set_many(self, entities: List[Entity]) -> List[Text]:
        """

        :param entities:
        :return:
        """
        type_name = entities[0].__class__.__name__
        records = self._get_serializer(type_name).serialize(entities, many=True)
        keys = [
            self._build_record_key(type_name, entity)
            for entity in entities
        ]
        if result := self.connection.set_many(dict(zip(keys, records))):
            return result

    def keys(self, cls: Type[Entity]) -> List[bytes]:
        """

        :param cls:
        :return:
        """
        return self.connection.keys(pattern=f'{cls.__name__}-*')
