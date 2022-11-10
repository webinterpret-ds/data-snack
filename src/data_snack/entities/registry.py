from dataclasses import dataclass
from typing import List, Text

from marshmallow.schema import SchemaMeta

from . import EntityType


@dataclass
class EntityRegistry:
    entity: EntityType
    schema: SchemaMeta
    keys: List[Text]
