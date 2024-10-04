import unittest
from dataclasses import is_dataclass
from datetime import datetime
from unittest.mock import patch

from histafrica.category.domain.entity import Category


class TestCategory(unittest.TestCase):

    def test_if_is_a_dataclas(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        with patch.object(Category, "validate") as mock_validate_method:
            category = Category(name="Movie")
            mock_validate_method.assert_called_once()

            self.assertEqual(category.name, "Movie")
            self.assertEqual(category.description, None)
            self.assertEqual(category.is_activate, True)
            self.assertIsInstance(category.created_at, datetime)
