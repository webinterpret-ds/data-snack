from dataclasses import dataclass

from data_snack.entities import Entity, set_entity_meta
import pytest


def test_set_entity_meta() -> None:
    keys = ["key_1", "key_2"]
    excluded_fields = ["excluded_1", "excluded_2", "excluded_3"]

    @set_entity_meta(keys=keys, excluded_fields=excluded_fields)
    @dataclass
    class DummyEntity(Entity):
        key_1: int
        key_2: int
        excluded_1: int
        excluded_2: int
        excluded_3: int
        included: int

    assert DummyEntity.Meta.keys == keys
    assert DummyEntity.Meta.excluded_fields == excluded_fields


def test_set_entity_meta_as_func() -> None:
    keys = ["key_1", "key_2"]
    excluded_fields = ["excluded_1", "excluded_2", "excluded_3"]

    @dataclass
    class PredefinedDummyEntity(Entity):
        key_1: int
        key_2: int
        excluded_1: int
        excluded_2: int
        excluded_3: int
        included: int

    set_entity_meta(PredefinedDummyEntity, keys=keys, excluded_fields=excluded_fields)

    assert PredefinedDummyEntity.Meta.keys == keys
    assert PredefinedDummyEntity.Meta.excluded_fields == excluded_fields


def test_set_entity_meta_keys_and_excluded_fields_not_found() -> None:
    with pytest.raises(LookupError):

        @set_entity_meta(keys=["non_existing_key"], excluded_fields=["non_existing_excluded_field"])
        @dataclass
        class DummyEntity(Entity):
            included: int


def test_set_entity_meta_as_func_keys_and_excluded_fields_not_found() -> None:
    @dataclass
    class PredefinedDummyEntity(Entity):
        included: int

    with pytest.raises(LookupError):
        set_entity_meta(
            PredefinedDummyEntity, keys=["non_existing_key"], excluded_fields=["non_existing_excluded_field"]
        )


def test_set_entity_meta_reset() -> None:
    with pytest.raises(ValueError):

        @set_entity_meta(keys=["wannabe_key_2"])
        @set_entity_meta(keys=["key_1"])
        @dataclass
        class DummyEntity(Entity):
            key_1: int
            wannabe_key_2: int
            included: int


def test_set_entity_meta_as_func_reset() -> None:
    @dataclass
    class PredefinedDummyEntity(Entity):
        key_1: int
        wannabe_key_2: int
        included: int

    set_entity_meta(PredefinedDummyEntity, keys=["key_1"])
    with pytest.raises(ValueError):
        set_entity_meta(PredefinedDummyEntity, keys=["wannabe_key_2"])


def test_set_entity_meta_dummy_set() -> None:
    @set_entity_meta
    class DummyEntity(Entity):
        included: int

    assert DummyEntity.Meta.keys == []
    assert DummyEntity.Meta.excluded_fields == []


def test_set_entity_meta_as_func_dummy_set() -> None:
    @dataclass
    class PredefinedDummyEntity(Entity):
        key_1: int

    set_entity_meta(PredefinedDummyEntity)
    set_entity_meta(PredefinedDummyEntity)

    assert PredefinedDummyEntity.Meta.keys == []
    assert PredefinedDummyEntity.Meta.excluded_fields == []


def test_set_entity_meta_instance_meta() -> None:
    keys = ["key"]
    excluded_fields = ["excluded"]

    @set_entity_meta(keys=keys, excluded_fields=excluded_fields)
    @dataclass
    class DummyEntity(Entity):
        key: int
        excluded: int
        included: int

    de = DummyEntity(1, 2, 3)
    assert de.Meta.keys == keys
    assert de.Meta.excluded_fields == excluded_fields


def test_set_entity_meta_as_func_instance_meta() -> None:
    keys = ["key"]
    excluded_fields = ["excluded"]

    @dataclass
    class PredefinedDummyEntity(Entity):
        key: int
        excluded: int
        included: int

    set_entity_meta(PredefinedDummyEntity, keys=keys, excluded_fields=excluded_fields)

    pde = PredefinedDummyEntity(1, 2, 3)
    assert pde.Meta.keys == keys
    assert pde.Meta.excluded_fields == excluded_fields


def test_set_entity_meta_instance_fields() -> None:
    key = 1
    excluded = 2
    included = 3

    @set_entity_meta(keys=["key"], excluded_fields=["excluded"])
    @dataclass
    class DummyEntity(Entity):
        key: int
        excluded: int
        included: int

    de = DummyEntity(key=key, excluded=excluded, included=included)
    assert de.key == key
    assert de.excluded == excluded
    assert de.included == included


def test_set_entity_meta_as_func_instance_fields() -> None:
    key = 1
    excluded = 2
    included = 3

    @dataclass
    class PredefinedDummyEntity(Entity):
        key: int
        excluded: int
        included: int

    set_entity_meta(PredefinedDummyEntity, keys=["key"], excluded_fields=["excluded"])

    pde = PredefinedDummyEntity(key=key, excluded=excluded, included=included)
    assert pde.key == key
    assert pde.excluded == excluded
    assert pde.included == included


def test_set_entity_meta_not_affect_base_class() -> None:
    @set_entity_meta(keys=["key"], excluded_fields=["excluded"])
    @dataclass
    class DummyEntity1(Entity):
        key: int
        excluded: int
        included: int

    @dataclass
    class DummyEntity2(Entity):
        key: int
        excluded: int
        included: int

    assert DummyEntity2.Meta.keys == []
    assert DummyEntity2.Meta.excluded_fields == []


def test_set_entity_meta_as_func_not_affect_base_class() -> None:
    @dataclass
    class PredefinedDummyEntity1(Entity):
        key: int
        excluded: int
        included: int

    @dataclass
    class PredefinedDummyEntity2(Entity):
        key: int
        excluded: int
        included: int

    set_entity_meta(PredefinedDummyEntity1, keys=["key"], excluded_fields=["excluded"])

    assert PredefinedDummyEntity2.Meta.keys == []
    assert PredefinedDummyEntity2.Meta.excluded_fields == []


def test_set_entity_meta_not_affect_entity_type() -> None:
    @set_entity_meta(keys=["key"], excluded_fields=["excluded"])
    @dataclass
    class DummyEntity1(Entity):
        key: int
        excluded: int
        included: int

    @dataclass
    class DummyEntity2(Entity):
        key: int
        excluded: int
        included: int

    # both classes are the abstract ones
    assert type(DummyEntity1) == type(DummyEntity2)


def test_set_entity_meta_as_func_not_affect_entity_type() -> None:
    @dataclass
    class PredefinedDummyEntity1(Entity):
        key: int
        excluded: int
        included: int

    @dataclass
    class PredefinedDummyEntity2(Entity):
        key: int
        excluded: int
        included: int

    set_entity_meta(PredefinedDummyEntity1, keys=["key"], excluded_fields=["excluded"])
    # both classes are the abstract ones
    assert type(PredefinedDummyEntity1) == type(PredefinedDummyEntity2)
