import ast
import zlib
from dataclasses import dataclass
from typing import Union, List

from data_snack.entities import Entity
from data_snack.serializers.base import Serializer


def _serialize(entity: Entity) -> bytes:
    return zlib.compress(str(list(entity.__dict__.values())).encode())


@dataclass
class DataclassSerializer(Serializer):

    def serialize(self, entity: Union[Entity, List[Entity]], many: bool=False) -> Union[bytes, List[bytes]]:
        return [_serialize(e) for e in entity] if many else _serialize(entity)

    def _deserialize(self, data: bytes) -> Entity:
        return self.entity_type(*ast.literal_eval(zlib.decompress(data).decode()))

    def deserialize(self, data: Union[bytes, List[bytes]], many: bool = False) -> Union[Entity, List[Entity]]:
        return [self._deserialize(d) for d in data] if many else self._deserialize(data)
