from typing import Dict, Type

from data_snack.entities import Entity
from data_snack.serializers import Serializer

EntityRegistry = Dict[Type[Entity], Serializer]

