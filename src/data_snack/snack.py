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
    A core interface handling saving and reading Entities from db.
    """

    connection: Connection
    registry: Dict[Text, EntityRegistry] = field(default_factory=dict)

    def register_entity(self, cls: Type[Entity], key_fields: List[Text], serializer: Serializer = None) -> None:
        """
        Registers new Entity type to Snack.

        :param cls: Entity type
        :param key_fields: a list of fields that will be used to define Entity key
        :param serializer: Serializer that is used to compress and decompress entities before saving in db
        """
        type_name = cls.__name__

        if type_name in self.registry:
            raise EntityAlreadyRegistered(f"Entity {type_name} is already registered")

        if not key_fields:
            raise WrongKeyValue("Entity keys cannot be empty")

        for key in key_fields:
            if key not in cls.__dataclass_fields__.keys():
                raise WrongKeyValue(f"Key {key} not found in entity definition.")

        if not serializer:
            serializer = DataclassSerializer(cls)

        self.registry[type_name] = EntityRegistry(
            entity_type=cls,
            serializer=serializer,
            key_fields=key_fields
        )

    def create_wrap(self, entity_type: Type[Entity], wrap_type: Type["Wrap"] = EntityWrap) -> "Wrap":
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
            for key in self.registry[type_name].key_fields
        ]
        return _build_key(type_name, *key_values)

    def set(self, entity: Entity) -> Optional[Text]:
        """
        Sets provided `Entity` object in db.
        Notice the entity stored in the db will be overwritten,
        so make sure all the combined keys are unique for each entity.

        :param entity: an entity to save
        :return: on success returns key used for the object, None on fail
        """
        type_name = entity.__class__.__name__
        key = self._build_record_key(type_name, entity)
        record = self._get_serializer(type_name).serialize(entity)
        if self.connection.set(key, record):
            return key

    def get(self, cls: Type[Entity], key_values: List[Text]) -> Entity:
        """
        Gets ane entity of `Entity` type from db based on provided key values.
        Notice, key is represented as a list of strings, since one Entity can have multiple key fields.

        :param cls: `Entity` type
        :param key_values: a list of key values representing the entity
        :return: a retrieved Entity object
        """
        type_name = cls.__name__
        _key = _build_key(type_name, *key_values)
        if value := self.connection.get(_key):
            return self._get_serializer(type_name).deserialize(value)
        else:
            raise KeyError(f"Key {_key} not found.")

    def get_many(self, cls: Type[Entity], keys_values: List[List[Text]]) -> List[Entity]:
        """
        Gets list of `Entity` objects from db based on provided list of keys.

        :param cls: `Entity` type
        :param keys_values: list of keys, each list defines a set key values for one Entity object
        :return: a list of retrieved Entity objects
        """
        type_name = cls.__name__
        _keys = [_build_key(type_name, *key_values) for key_values in keys_values]
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
        keys = [
            self._build_record_key(type_name, entity)
            for entity in entities
        ]
        if result := self.connection.set_many(dict(zip(keys, records))):
            return result

    def keys(self, cls: Type[Entity]) -> List[Text]:
        """
        Gets a list of keys for a given Entity type.

        :param cls: Entity type
        :return: a list of keys
        """
        return self.connection.keys(pattern=f'{cls.__name__}-*')
