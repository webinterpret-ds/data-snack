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
            (Car, ["1"], "c35a43010ddc80cf23173315516062be"),
            (Car, [1], "c35a43010ddc80cf23173315516062be"),  # the same hash as above
            (Car, ["Abc"], "35b8a98d4b40102ed1f501e290f76684"),
            (Car, [1.0], "fcd81df24fc6afd906a74c87560aa69b"),
            (Car, [True], "e919cd976a717fe3df3a6bbbbdae54e1"),
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

        expected = "75a88f65b9eb4f207e094cf072acc7e7"

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

        expected_keys = [Car, DummyEntity]
        expected_values = [1, 2]

        # act
        dct = {Car: 1, DummyEntity: 2}

        # assert
        self.assertEqual(list(dct.keys()), expected_keys)
        self.assertEqual(list(dct.values()), expected_values)
