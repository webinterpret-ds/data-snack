from unittest import TestCase

from parameterized import parameterized

from data_snack.key_factories import KeyFactory
from data_snack.key_factories.cluster import ClusterKeyFactory


class TestClusterKeyFactory(TestCase):
    def setUp(self) -> None:
        self.key_factory = ClusterKeyFactory()

    @parameterized.expand(
        [
            ("Entity", ["1"], "{Entity}-1"),
            ("Entity", [1], "{Entity}-1"),
            ("Entity", ["Abc"], "{Entity}-Abc"),
        ]
    )
    def test_get_key_single_key_value(self, type_name, key_values, expected) -> None:
        # act
        actual = self.key_factory.get_key(type_name, *key_values)

        # assert
        self.assertEqual(actual, expected)

    def test_get_key_multiple_key_values(self) -> None:
        # arrange
        type_name = "Entity"
        key_values = [1, "2", "A", "Bcd"]

        expected = "{Entity}-1_2_A_Bcd"

        # act
        actual = self.key_factory.get_key(type_name, *key_values)

        # assert
        self.assertEqual(actual, expected)

    def test_get_pattern_default(self) -> None:
        # arrange
        type_name = "Entity"

        expected = "{Entity}-*"

        # act
        actual = self.key_factory.get_pattern(type_name)

        # assert
        self.assertEqual(actual, expected)

    def test_get_pattern_custom(self) -> None:
        # arrange
        type_name = "Entity"
        pattern = "custom*"

        expected = "{Entity}-custom*"

        # act
        actual = self.key_factory.get_pattern(type_name, pattern=pattern)

        # assert
        assert expected == actual
