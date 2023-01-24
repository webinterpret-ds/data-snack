from dataclasses import dataclass
from typing import Type

from ..serializers import Serializer
from . import Entity


@dataclass
class EntityRegistry:
    # TODO: currently Entity.Meta.keys can be edited after initialization, it should be handled somehow.
    entity_type: Type[Entity]
    serializer: Serializer
