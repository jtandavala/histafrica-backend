import unittest
from typing import Optional

from histafrica.shared.application.dto import Filter, SearchInput


class TestSearchInput(unittest.TestCase):
    def test_fields(self):
        self.assertEqual(
            SearchInput.__annotations__,
            {
                "page": Optional[int],
                "per_page": Optional[int],
                "sort": Optional[str],
                "sort_dir": Optional[str],
                "filter": Optional[Filter],
            },
        )
