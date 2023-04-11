import ast
import zlib
from dataclasses import dataclass
from typing import List, Optional, Union, get_type_hints

import pandas as pd

from data_snack.entities import Entity
from data_snack.serializers.base import Serializer


@dataclass
class DataclassSerializer(Serializer):
    def __post_init__(self):
        self.entity_fields = list(get_type_hints(self.entity_type).keys())

    def _serialize(self, entity: Optional[Entity]) -> Optional[bytes]:
        entity_fields = entity.__dict__
        values = [
            entity_fields[field] if pd.notnull(entity_fields[field]) else None
            for field in self.entity_fields
        ]
        return zlib.compress(str(values).encode())

    def serialize(
        self, entity: Union[Entity, List[Entity]], many: bool = False
    ) -> Union[bytes, List[bytes]]:
        return [self._serialize(e) for e in entity] if many else self._serialize(entity)

    def _deserialize(self, data: Optional[bytes]) -> Optional[Entity]:
        if not data:
            return
        return self.entity_type(*ast.literal_eval(zlib.decompress(data).decode()))

    def deserialize(
        self, data: Union[Optional[bytes], List[Optional[bytes]]], many: bool = False
    ) -> Union[Optional[Entity], List[Optional[Entity]]]:
        return [self._deserialize(d) for d in data] if many else self._deserialize(data)
