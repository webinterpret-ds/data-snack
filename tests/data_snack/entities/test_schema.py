from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, List, Optional, Type

import pytest

from data_snack.entities import Entity
from data_snack.entities.schema import get_entity_schema


@pytest.fixture
def dummy_entity() -> Type[Entity]:
    @dataclass
    class DummyEntity(Entity):
        key: int
        excluded: int
        integer: int
        floating: float
        string: str
        boolean: bool
        any: Any
        optional_any: Optional[Any]
        time_: date
        datetime_: datetime

        class Meta:
            keys: List[str] = ["key"]
            excluded_fields: List[str] = ["excluded"]

    return DummyEntity


def test_get_entity_schema_all_fields(dummy_entity: Type[Entity]) -> None:
    """Testing if `get_entity_schema` recognizes types properly."""
    result = get_entity_schema(entity_type=dummy_entity, exclude_fields=False)
    expected = {
        "key": int,
        "excluded": int,
        "integer": int,
        "floating": float,
        "string": str,
        "boolean": bool,
        "any": Any,
        "optional_any": Optional[Any],
        "time_": date,
        "datetime_": datetime,
    }
    assert result == expected


def test_get_entity_schema_exclude_fields(dummy_entity: Type[Entity]) -> None:
    """Testing if `get_entity_schema` filters out entity excluded fields properly."""
    result = get_entity_schema(entity_type=dummy_entity, exclude_fields=True)
    expected = {
        "key": int,
        "integer": int,
        "floating": float,
        "string": str,
        "boolean": bool,
        "any": Any,
        "optional_any": Optional[Any],
        "time_": date,
        "datetime_": datetime,
    }
    assert result == expected
