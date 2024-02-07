from dataclasses import dataclass, asdict
from typing import List, Optional, Union, Dict

from data_snack.entities import Entity
from data_snack.serializers.base import Serializer


@dataclass
class JsonSerializer(Serializer):

    def _serialize(self, entity: Optional[Entity]) -> Optional[Dict]:
        return asdict(entity)

    def serialize(
            self, entity: Union[Entity, List[Entity]], many: bool = False
    ) -> Union[Dict, List[Dict]]:
        return [self._serialize(e) for e in entity] if many else self._serialize(entity)

    def _deserialize(self, data: Optional[Dict]) -> Optional[Entity]:
        if not data:
            return
        return self.entity_type(**data)

    def deserialize(
            self, data: Union[Optional[Dict], List[Optional[Dict]]], many: bool = False
    ) -> Union[Optional[Entity], List[Optional[Entity]]]:
        return [self._deserialize(d) for d in data] if many else self._deserialize(data)

