from abc import ABC
from typing import Any


class Entity(ABC):
    def __init__(self, *args: Any, **kwargs: Any):
        ...
