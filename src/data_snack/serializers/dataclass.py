import ast
import zlib
from dataclasses import dataclass
from typing import List, Union, get_type_hints

from data_snack.entities import Entity
from data_snack.serializers.base import Serializer


@dataclass
class DataclassSerializer(Serializer):
    def __post_init__(self):
        self.entity_fields = list(get_type_hints(self.entity_type).keys())

    def _serialize(self, entity: Entity) -> bytes:
        entity_fields = entity.__dict__
        values = [entity_fields[field] for field in self.entity_fields]
        return zlib.compress(str(values).encode())

    def serialize(
        self, entity: Union[Entity, List[Entity]], many: bool = False
    ) -> Union[bytes, List[bytes]]:
        return [self._serialize(e) for e in entity] if many else self._serialize(entity)

    def _deserialize(self, data: bytes) -> Entity:
        return self.entity_type(*ast.literal_eval(zlib.decompress(data).decode()))

    def deserialize(
        self, data: Union[bytes, List[bytes]], many: bool = False
    ) -> Union[Entity, List[Entity]]:
        return [self._deserialize(d) for d in data] if many else self._deserialize(data)
