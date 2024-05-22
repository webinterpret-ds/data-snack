from dataclasses import dataclass
from unittest import TestCase

from parameterized import parameterized

from data_snack.entities import Entity
from data_snack.key_factories.non_cluster import NonClusterKey
from tests.data_snack.conftest import Car


class TestNonClusterKeyFactory(TestCase):
    def setUp(self) -> None:
        self.key_factory = NonClusterKey

    @parameterized.expand(
        [
            (Car, ["1"], "Car-1-1"),
            (Car, [1], "Car-1-1"),
            (Car, ["Abc"], "Car-1-Abc"),
            (Car, [1.0], "Car-1-1.0"),
            (Car, [True], "Car-1-True"),
        ]
    )
    def test_keystring_single_key_value(self, entity_type, key_values, expected) -> None:
        # act
        actual = self.key_factory(entity_type, key_values).keystring

        # assert
        assert expected == actual

    def test_keystring_multiple_key_values(self) -> None:
        # arrange
        entity_type = Car
        key_values = [1, "2", "A", "Bcd"]

        expected = "Car-1-1_2_A_Bcd"

        # act
        actual = self.key_factory(entity_type, key_values).keystring

        # assert
        assert expected == actual

    def test_get_pattern_default(self) -> None:
        # arrange
        entity_type = Car

        expected = "Car-1-*"

        # act
        actual = self.key_factory(entity_type, ["1"]).get_pattern()

        # assert
        assert expected == actual

    def test_get_pattern_custom(self) -> None:
        # arrange
        entity_type = Car
        pattern = "custom*"

        expected = "Car-1-custom*"

        # act
        actual = self.key_factory(entity_type, ["1"]).get_pattern(pattern=pattern)

        # assert
        assert expected == actual

    def test_hashable(self) -> None:
        # arrange
        @dataclass
        class DummyEntity(Entity):
            field: int

            class Meta:
                keys = ["field"]
                excluded_fields = []
                version = 1

        expected_keys = [Car, DummyEntity]
        expected_values = [1, 2]

        # act
        dct = {Car: 1, DummyEntity: 2}

        # assert
        self.assertEqual(list(dct.keys()), expected_keys)
        self.assertEqual(list(dct.values()), expected_values)