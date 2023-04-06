from dataclasses import dataclass, field
from typing import Dict, List, Optional, Text, Type, Any

from .connections import Connection
from .entities import Entity, EntityRegistry
from .exceptions import EntityAlreadyRegistered, WrongKeyValue
from .key_factory import KeyFactory, key_factory
from .serializers import DataclassSerializer, Serializer
from .wrap import EntityWrap


@dataclass
class Snack:
    """
    A core interface handling saving and reading Entities from db.
    """

    connection: Connection
    registry: Dict[Text, EntityRegistry] = field(default_factory=dict)
    key_factory: KeyFactory = field(default=key_factory)

    def register_entity(
        self,
        entity_type: Type[Entity],
        serializer: Serializer = None,
    ) -> None:
        """
        Registers new Entity type to Snack.

        :param entity_type: Entity type
        :param serializer: Serializer that is used to compress and decompress entities before saving in db
        """
        type_name = entity_type.__name__

        if type_name in self.registry:
            raise EntityAlreadyRegistered(f"Entity {type_name} is already registered")

        if not serializer:
            serializer = DataclassSerializer(entity_type)

        self.registry[type_name] = EntityRegistry(
            entity_type=entity_type, serializer=serializer
        )

    def create_wrap(
        self, entity_type: Type[Entity], wrap_type: Type["Wrap"] = EntityWrap
    ) -> "Wrap":
        """
        Creates a Wrap object for selected Entity type.

        :param entity_type: Entity type
        :param wrap_type: `Wrap` type, by default it uses `EntityWrap`, but any other `Wrap` can be used
        :return: created Wrap object
        """
        return wrap_type(self, entity_type)

    def _get_serializer(self, type_name: Text) -> Serializer:
        return self.registry[type_name].serializer

    def _build_record_key(self, type_name: Text, entity: Entity) -> Text:
        key_values = [
            getattr(entity, key)
            for key in self.registry[type_name].entity_type.get_keys()
        ]
        return self.key_factory(type_name, *key_values)

    def set(self, entity: Entity, expire: int = 0) -> Optional[Text]:
        """
        Sets provided `Entity` object in db.
        Notice the entity stored in the db will be overwritten,
        so make sure all the combined keys are unique for each entity.

        :param entity: an entity to save
        :param expire: number of seconds until the item is expired, or zero for no expiry
        :return: on success returns key used for the object, None on fail
        """
        type_name = entity.__class__.__name__
        key = self._build_record_key(type_name, entity)
        record = self._get_serializer(type_name).serialize(entity)
        if self.connection.set(key, record, expire):
            return key

    def get(self, cls: Type[Entity], key_values: List[Any]) -> Optional[Entity]:
        """
        Gets ane entity of `Entity` type from db based on provided key values.
        Notice, key is represented as a list of strings, since one Entity can have multiple key fields.

        :param cls: `Entity` type
        :param key_values: a list of key values representing the entity
        :return: a retrieved Entity object
        """
        type_name = cls.__name__
        _key = self.key_factory(type_name, *key_values)
        value = self.connection.get(_key)
        return self._get_serializer(type_name).deserialize(value)

    def delete(self, cls: Type[Entity], key_values: List[Any]) -> bool:
        """
        Deletes one entity of `Entity` type from db based on provided key values.
        Notice, key is represented as a list of strings, since one Entity can have multiple key fields.

        :param cls: `Entity` type
        :param key_values: a list of key values representing the entity
        :return: True if data were deleted
        """
        type_name = cls.__name__
        _key = self.key_factory(type_name, *key_values)
        return self.connection.delete(_key)

    def get_many(
        self, cls: Type[Entity], keys_values: List[List[Any]]
    ) -> List[Optional[Entity]]:
        """
        Gets list of `Entity` objects from db based on provided list of keys.

        :param cls: `Entity` type
        :param keys_values: list of keys, each list defines a set key values for one Entity object
        :return: a list of retrieved Entity objects
        """
        type_name = cls.__name__
        _keys = [self.key_factory(type_name, *key_values) for key_values in keys_values]
        records = list(self.connection.get_many(_keys).values())
        return self._get_serializer(type_name).deserialize(records, many=True)

    def set_many(self, entities: List[Entity]) -> List[Text]:
        """
        Saves multiple `Entity` objects in db.

        :param entities: a list of Entity objects
        :return: a list of keys generated for saved objects
        """
        type_name = entities[0].__class__.__name__
        records = self._get_serializer(type_name).serialize(entities, many=True)
        keys = [self._build_record_key(type_name, entity) for entity in entities]
        if result := self.connection.set_many(dict(zip(keys, records))):
            return result

    def delete_many(self, cls: Type[Entity], keys_values: List[List[Any]]) -> bool:
        """
        Deletes multiple `Entity` objects in db.

        :param cls: `Entity` type
        :param keys_values: list of keys, each list defines a set key values for one Entity object
        :return: True if data were deleted
        """
        type_name = cls.__name__
        _keys = [self.key_factory(type_name, *key_values) for key_values in keys_values]
        return self.connection.delete_many(_keys)

    def keys(self, cls: Type[Entity]) -> List[Text]:
        """
        Gets a list of keys for a given Entity type.

        :param cls: Entity type
        :return: a list of keys
        """
        return self.connection.keys(pattern=f"{cls.__name__}-*")
