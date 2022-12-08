from dataclasses import dataclass
from typing import List, Text, Type

from . import Entity
from ..serializers import Serializer


@dataclass
class EntityRegistry:
    entity_type: Type[Entity]
    serializer: Serializer
    key_fields: List[Text]
