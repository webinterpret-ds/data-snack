from typing import Type, Dict

from data_snack.entities import Entity
from data_snack.serializers import Serializer

EntityRegistry = Dict[Type[Entity], Serializer]

# @dataclass
# class EntityRegistry:
#     # TODO: currently Entity.Meta.keys can be edited after initialization, it should be handled somehow.
#     entity_type: Type[Entity]
#     serializer: Serializer
