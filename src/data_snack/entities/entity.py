from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass
class Entity(ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        ...
