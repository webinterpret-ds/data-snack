from dataclasses import dataclass
from typing import List, Text, Type

from ..serializers import Serializer
from . import Entity


@dataclass
class EntityRegistry:
    entity_type: Type[Entity]
    serializer: Serializer
    key_fields: List[Text]
