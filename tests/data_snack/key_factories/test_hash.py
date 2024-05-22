from dataclasses import dataclass
from typing import Any
from unittest import TestCase

from parameterized import parameterized

from data_snack.entities import Entity
from data_snack.key_factories.hash import HashKey
from tests.data_snack.conftest import Car


class TestHashKeyFactory(TestCase):
    def setUp(self) -> None:
        self.key_factory = HashKey

    @parameterized.expand(
        [
            (Car, ["1"], "3680a79e3be34d33bdedf809038f4ef7"),
            (Car, [1], "3680a79e3be34d33bdedf809038f4ef7"),  # the same hash as above
            (Car, ["Abc"], "31192f88d3779695c98ed4b587e9c338"),
            (Car, [1.0], "577c714950bfb0996aa39966f471adfc"),
            (Car, [True], "8ad89063904776f49b9eac62191d0c81"),
        ]
    )
    def test_keystring_single_key_value(self, entity_type, key_values, expected) -> None:
        # act
        actual = self.key_factory(entity_type, key_values).keystring

        # assert
        self.assertEqual(actual, expected)

    def test_keystring_multiple_key_values(self) -> None:
        # arrange
        entity_type = Car
        key_values = [1, "2", "A", "Bcd"]

        expected = "61c1d9a9ee6970313566ca1d66e5d216"

        # act
        actual = self.key_factory(entity_type, key_values).keystring

        # assert
        self.assertEqual(actual, expected)

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
