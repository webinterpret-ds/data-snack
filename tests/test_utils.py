from dataclasses import dataclass
from typing import Optional
from unittest import TestCase

from parameterized import parameterized

from data_snack.utils import get_attribute_of_first_element_from_iterable


class TestGetAttributeOfFirstElementFromIterable(TestCase):
    def setUp(self) -> None:
        self.func = get_attribute_of_first_element_from_iterable

    @parameterized.expand(
        [
            ("attribute found", "attr", 1),
            ("attribute not found", "nonexistent", None),
        ]
    )
    def test_func_when_iterable_not_empty_expect_proper_output(
        self, name: str, attribute_name: str, expected: Optional[int]
    ) -> None:
        # arrange
        @dataclass
        class DummyClass:
            attr: int

        dummy_instance_1 = DummyClass(attr=1)
        dummy_instance_2 = DummyClass(attr=2)

        list_of_dummy_instances = [dummy_instance_1, dummy_instance_2]

        # act
        result = self.func(iterable=list_of_dummy_instances, attribute_name=attribute_name)

        # assert
        self.assertEqual(result, expected)

    def test_func_when_iterable_empty_expect_none(self) -> None:
        # act
        result = self.func(iterable=[], attribute_name="doesnt_matter")

        # assert
        self.assertIsNone(result)
