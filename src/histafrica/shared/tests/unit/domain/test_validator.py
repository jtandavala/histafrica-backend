import unittest

from histafrica.shared.domain.validators import ValidatorRules


class TestValidatorRules(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.values("some value", "prop")
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, "some value")
        self.assertEqual(validator.prop, "prop")
