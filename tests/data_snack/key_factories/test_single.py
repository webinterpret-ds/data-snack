from unittest import TestCase

from parameterized import parameterized

from data_snack.key_factories.single import SingleKeyFactory


class TestSingleKeyFactory(TestCase):
    def setUp(self) -> None:
        self.key_factory = SingleKeyFactory()

    @parameterized.expand(
        [
            ("Entity", ["1"], "Entity-1"),
            ("Entity", [1], "Entity-1"),
            ("Entity", ["Abc"], "Entity-Abc"),
        ]
    )
    def test_get_key_single_value(self, type_name, key_values, expected):
        # act
        actual = self.key_factory.get_key(type_name, *key_values)

        # assert
        assert expected == actual

    def test_get_key_multiple_values(self):
        # arrange
        type_name = "Entity"
        key_values = [1, "2", "A", "Bcd"]

        expected = "Entity-1_2_A_Bcd"

        # act
        actual = self.key_factory.get_key(type_name, *key_values)

        # assert
        assert expected == actual

    def test_get_pattern(self):
        # arrange
        type_name = "Entity"

        expected = "Entity-*"

        # act
        actual = self.key_factory.get_pattern(type_name)

        # assert
        assert expected == actual
