from dataclasses import dataclass
from typing import List, Text

from . import EntityType
from ..serializers import Serializer


@dataclass
class EntityRegistry:
    entity: EntityType
    serializer: Serializer
    keys: List[Text]
