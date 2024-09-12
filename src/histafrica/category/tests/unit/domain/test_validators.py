import os
import unittest
import django

from histafrica.category.domain.validators import (
    CategoryValidator,
    CategoryValidatorFactory,
)


class TestCategoryValidator(unittest.TestCase):
    validator: CategoryValidator

    @classmethod
    def setUpClass(cls) -> None:
        # Set the settings module for Django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "framework.settings")
        django.setup()  # Initialize Django
        super().setUpClass()

    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory.create()
        return super().setUp()

    def test_invalidation_cases_for_name_field(self):
        invalid_data = [
            {"data": None, "expected": "This field is required."},
            {"data": {}, "expected": "This field is required."},
            {"data": {"name": None}, "expected": "This field may not be null."},
            {"data": {"name": ""}, "expected": "This field may not be blank."},
            {"data": {"name": 5}, "expected": "Not a valid string."},
            {
                "data": {"name": "a" * 256},
                "expected": "Ensure this field has no more than 255 characters.",
            },
        ]

        for i in invalid_data:
            is_valid = self.validator.validate(i["data"])
            self.assertFalse(is_valid)
