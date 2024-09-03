import unittest
from typing import List, Optional

from histafrica.shared.application.dto import (
    Filter,
    Item,
    PaginationOutput,
    PaginationOutputMapper,
    SearchInput,
)


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


class TestPaginationOut(unittest.TestCase):

    def test_fields(self):
        self.assertEqual(
            PaginationOutput.__annotations__,
            {
                "items": List[Item],
                "total": int,
                "per_page": int,
                "current_page": int,
                "last_page": int,
            },
        )


class PaginationOutputChild(PaginationOutput):
    pass


class TestPaginationOutputMapper(unittest.TestCase):

    def test_from_child(self):
        mapper = PaginationOutputMapper.from_child(PaginationOutputChild)

        self.assertIsInstance(mapper, PaginationOutputMapper)
        self.assertTrue(issubclass(mapper.output_child, PaginationOutputChild))
