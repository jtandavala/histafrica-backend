import unittest
import uuid
from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
from unittest.mock import patch

from histafrica.shared.domain.exceptions import InvalidUuidException
from histafrica.shared.domain.value_objects import UniqueEntityId, ValueObject


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

    def test_convert_to_string(self):
        vo1 = StubOneProp(prop="value")
        self.assertEqual(vo1.prop, str(vo1))

        vo2 = StubTwoProp(prop1="value1", prop2="value2")
        self.assertEqual('{"prop1": "value1", "prop2": "value2"}', str(vo2))

    def test_init_prop(self):
        vo1 = StubOneProp(prop="value")
        self.assertEqual(vo1.prop, "value")

        vo2 = StubTwoProp(prop1="value1", prop2="value2")
        self.assertEqual(vo2.prop1, "value1")
        self.assertEqual(vo2.prop2, "value2")

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = StubOneProp(prop="value")
            value_object.prop = "fake"


class TestUniqueEntityId(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId("fake id")
            mock_validate.assert_called_once()
            self.assertEqual(assert_error.exception.args[0], "ID must be a valid UUID")

    def test_generate_id_when_pass_no_id_in_constroctor(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_affect=UniqueEntityId._UniqueEntityId__validate,
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "fake id"
