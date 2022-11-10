from dataclasses import dataclass
from typing import TypeVar


@dataclass
class Entity:
    ...


EntityType = TypeVar('EntityType', bound=Entity)
