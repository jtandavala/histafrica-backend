import unittest

from histafrica.shared.domain.exceptions import ValidationException
from histafrica.shared.domain.validators import ValidatorRules


class TestValidatorRules(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.values("some value", "prop")
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, "some value")
        self.assertEqual(validator.prop, "prop")

    def test_requred_rule(self):
        invalid_data = [{"value": None, "prop": "prop"}, {"value": "", "prop": "prop"}]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(i["value"], i["prop"]).required()
                self.assertEqual("The prop is required", assert_error.exception.args[0])
