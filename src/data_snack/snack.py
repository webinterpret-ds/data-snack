from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Union

from data_snack.connections import Connection
from data_snack.entities import Entity, EntityRegistry
from data_snack.entities.compound import CompoundEntity
from data_snack.entities.utils import map_values
from data_snack.exceptions import EntityAlreadyRegistered
from data_snack.key_factories import Key, NonClusterKey
from data_snack.serializers import DataclassSerializer, Serializer
from data_snack.utils import get_attribute_of_first_element_from_iterable
from data_snack.wrap import EntityWrap


def _apply_mask(values: List[Any], mask: List[bool]) -> List[Any]:
    return [values[i] for i, m in enumerate(mask) if m]


@dataclass
class Snack:
    """
    A core interface handling saving and reading Entities from db.
    """

    connection: Connection
    registry: EntityRegistry = field(default_factory=dict)
    key_factory: Type[Key] = field(default=NonClusterKey)

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
        if entity_type in self.registry:
            raise EntityAlreadyRegistered(f"Entity named {entity_type.__name__} is already registered")

        if not serializer:
            serializer = DataclassSerializer(entity_type)

        self.registry[entity_type] = serializer

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

    def _get_serializer(self, entity_type: Type[Entity]) -> Serializer:
        return self.registry[entity_type]

    def _build_record_key(self, entity: Entity) -> Key:
        entity_type = entity.__class__
        if entity_type not in self.registry:
            raise Exception(f"Entity named {entity_type.__name__} is not registered.")
        key_values = [getattr(entity, key) for key in entity_type.get_keys()]
        return self.key_factory(entity.__class__, key_values)

    def set(self, entity: Entity) -> Optional[str]:
        """
        Sets provided `Entity` object in db.
        Notice the entity stored in the db will be overwritten,
        so make sure all the combined keys are unique for each entity.

        :param entity: an entity to save
        :return: on success returns key used for the object, None on fail
        """
        key = self._build_record_key(entity)
        record = self._get_serializer(entity.__class__).serialize(entity)
        if self.connection.set(key, record):
            return key.keystring  # Should we return keystring or maybe just a key?

    def _get(self, cls: Type[Entity], key_values: List[Any]) -> Optional[Entity]:
        """
        Gets ane entity of `Entity` type from db based on provided key values.

        :param cls: `Entity` type
        :param key_values: a list of key values representing the entity
        :return: a retrieved Entity object
        """
        _key = self.key_factory(cls, key_values)
        value = self.connection.get(_key)
        return self._get_serializer(cls).deserialize(value)

    def _get_compound(self, cls: Type[CompoundEntity], key_values: List[Any]) -> Optional[CompoundEntity]:
        """
        Gets ane entity of `CompoundEntity` type as collection of source entities based on provided key values.

        :param cls: `CompoundEntity` type
        :param key_values: a list of key values representing the compound entity
        :return: a retrieved CompoundEntity object
        """
        source_entities = []
        source_entities_fields_mappings = []
        mandatory_source_entities_mask = []
        for source in cls.Meta.sources:  # TODO: parallelize processing for multiple sources
            mapped_keys = map_values(source.fields_mapping, cls.get_keys())
            mapped_key_values = [key_values[mapped_keys.index(key)] for key in source.entity.get_keys()]
            source_entities.append(self._get(source.entity, mapped_key_values))
            source_entities_fields_mappings.append(source.entity_fields_mapping)
            mandatory_source_entities_mask.append(not source.optional)
        return (
            cls.create_from_source_entities(source_entities, source_entities_fields_mappings, key_values)
            if all(_apply_mask(source_entities, mandatory_source_entities_mask)) else None
        )

    def get(
            self, cls: Union[Type[Entity], Type[CompoundEntity]], key_values: List[Any]
    ) -> Optional[Union[Entity, CompoundEntity]]:
        """
        Gets one entity depending on type from db based on provided key values.
        Notice, key is represented as a list of strings, since one entity can have multiple key fields.

        :param cls: `Entity` or `CompoundEntity` type
        :param key_values: a list of key values representing the entity
        :return: a retrieved `Entity` or `CompoundEntity` object
        """
        if issubclass(cls, Entity):
            return self._get(cls, key_values)
        elif issubclass(cls, CompoundEntity):
            return self._get_compound(cls, key_values)

    def delete(self, cls: Type[Entity], key_values: List[Any]) -> bool:
        """
        Deletes one entity of `Entity` type from db based on provided key values.
        Notice, key is represented as a list of strings, since one Entity can have multiple key fields.

        :param cls: `Entity` type
        :param key_values: a list of key values representing the entity
        :return: True if data were deleted
        """
        _key = self.key_factory(cls, key_values)
        return self.connection.delete(_key)

    def _get_many(
        self, cls: Type[Entity], keys_values: List[List[Any]]
    ) -> List[Optional[Entity]]:
        """
        Gets list of `Entity` objects from db based on provided list of keys.

        :param cls: `Entity` type
        :param keys_values: list of keys, each list defines a set key values for one Entity object
        :return: a list of retrieved Entity objects
        """
        _keys = [self.key_factory(cls, key_values) for key_values in keys_values]
        results_unordered = self.connection.get_many(_keys)
        records_ordered = [results_unordered.get(key.keystring) for key in _keys]
        return self._get_serializer(cls).deserialize(records_ordered, many=True)

    def _get_many_compound(
        self, cls: Type[CompoundEntity], keys_values: List[List[Any]]
    ) -> List[Optional[CompoundEntity]]:
        """
        Gets list of `CompoundEntity` objects as collections of source entities based on provided key values.

        :param cls: `CompoundEntity` type
        :param keys_values: list of keys, each list defines a set key values for one CompoundEntity object
        :return: a list of retrieved CompoundEntity objects
        """
        source_entities = []
        source_entities_fields_mappings = []
        mandatory_source_entities_mask = []
        for source in cls.Meta.sources:
            mapped_keys = map_values(source.fields_mapping, cls.get_keys())
            mapped_keys_values = [
                [
                    key_values[mapped_keys.index(key)] for key in source.entity.get_keys()
                ]
                for key_values in keys_values
            ]
            source_entities.append(self._get_many(source.entity, mapped_keys_values))
            source_entities_fields_mappings.append(source.entity_fields_mapping)
            mandatory_source_entities_mask.append(not source.optional)
        return [
            cls.create_from_source_entities(entities, source_entities_fields_mappings, key_values)
            if all(_apply_mask(entities, mandatory_source_entities_mask)) else None
            for entities, key_values in zip(zip(*source_entities), keys_values)
        ]

    def get_many(
        self, cls: Union[Type[Entity], Type[CompoundEntity]], keys_values: List[List[Any]]
    ) -> List[Optional[Union[Entity, CompoundEntity]]]:
        """
        Gets list of entity objects depending on type from db based on provided key values.
        Notice, key is represented as a list of strings, since one entity can have multiple key fields.

        :param cls: `Entity` or `CompoundEntity` type
        :param keys_values: list of keys, each list defines a set key values for one entity object
        :return: a list of retrieved `Entity` or `CompoundEntity` objects
        """
        if issubclass(cls, Entity):
            return self._get_many(cls, keys_values)
        elif issubclass(cls, CompoundEntity):
            return self._get_many_compound(cls, keys_values)

    def set_many(self, entities: List[Entity]) -> Any:
        """
        Saves multiple `Entity` objects in db.

        :param entities: a list of Entity objects
        :return: a list of keys generated for saved objects
        """
        if (entity_type := get_attribute_of_first_element_from_iterable(entities, "__class__")) is type(None):
            return
        records = self._get_serializer(entity_type).serialize(entities, many=True)
        keys = [self._build_record_key(entity) for entity in entities]
        if result := self.connection.set_many(dict(zip(keys, records))):
            return result

    def delete_many(self, cls: Type[Entity], keys_values: List[List[Any]]) -> bool:
        """
        Deletes multiple `Entity` objects in db.

        :param cls: `Entity` type
        :param keys_values: list of keys, each list defines a set key values for one Entity object
        :return: True if data were deleted
        """
        _keys = [
            self.key_factory(cls, key_values)
            for key_values in keys_values
        ]
        return self.connection.delete_many(_keys)

    def keys(self, cls: Type[Entity]) -> List[str]:
        """
        Gets a list of keys for a given Entity type.

        :param cls: Entity type
        :return: a list of keys
        """
        return self.connection.keys(pattern=self.key_factory(cls, []).get_pattern("*"))
