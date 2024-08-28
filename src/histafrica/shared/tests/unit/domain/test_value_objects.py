import unittest
from abc import ABC
from dataclasses import dataclass, is_dataclass

from histafrica.shared.domain.value_objects import ValueObject


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubOneProp(prop="value")
        self.assertEqual(vo1.prop, "value")

        vo2 = StubTwoProp(prop1="value1", prop2="value2")
        self.assertEqual(vo2.prop1, "value1")
        self.assertEqual(vo2.prop2, "value2")
