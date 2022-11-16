from typing import TypeVar
from pydantic.dataclasses import dataclass


@dataclass
class Entity:
    ...


EntityType = TypeVar('EntityType', bound=Entity)
