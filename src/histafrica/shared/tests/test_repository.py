import unittest
from dataclasses import dataclass
from typing import Optional

from histafrica.shared.domain.entity import Entity
from histafrica.shared.domain.exceptions import NotFoundException
from histafrica.shared.domain.repository import (
    Filter,
    InMemoryRepository,
    RepositoryInterface,
    SearchableRepositoryInterface,
    SearchParams,
)
from histafrica.shared.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface with abstract "
            + "methods delete, find_all, find_by_id, insert, update",
        )


@dataclass(frozen=True, kw_only=True, slots=True)
class StubEntity(Entity):
    name: str
    price: float


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    pass


class TestInMemoryRepository(unittest.TestCase):

    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repo.items, [])

    def test_insert(self):
        entity = StubEntity(name="test", price=5)
        self.repo.insert(entity)
        self.assertEqual(self.repo.items[0], entity)

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id("fake id")
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'"
        )

        unique_entity_id = UniqueEntityId("af46842e-027d-4c91-b259-3a3642144ba4")
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'af46842e-027d-4c91-b259-3a3642144ba4'",
        )

    def test_find_by_id(self):
        entity = StubEntity(name="test", price=5)
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity)

    def test_find_all(self):
        entity = StubEntity(name="test", price=5)
        self.repo.insert(entity)
        items = self.repo.find_all()
        self.assertEqual(items, [entity])

    def test_throw_not_found_exception_in_update(self):
        entity = StubEntity(name="test", price=5)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'"
        )

    def test_update(self):
        entity = StubEntity(name="test", price=5)
        self.repo.insert(entity)

        entity_updated = StubEntity(
            unique_entity_id=entity.unique_entity_id, name="updated", price=1
        )
        self.repo.update(entity_updated)

        self.assertEqual(entity_updated, self.repo.items[0])

    def test_throw_not_found_exception_in_delete(self):
        entity = StubEntity(name="test", price=5)
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(entity)
        self.assertEqual(
            assert_error.exception.args[0], f"Entity not found using ID '{entity.id}'"
        )

    def test_delete(self):
        entity = StubEntity(name="test", price=5)
        self.repo.insert(entity)

        self.repo.delete(entity)
        self.assertEqual(self.repo.items, [])


class TestSearchableRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            SearchableRepositoryInterface()
        self.assertEqual(
            "Can't instantiate abstract class SearchableRepositoryInterface "
            "with abstract "
            "methods delete, find_all, find_by_id, insert, search, update",
            assert_error.exception.args[0],
        )

    def test_sortable_fields_prop(self):
        self.assertEqual(SearchableRepositoryInterface.sortable_fields, [])


class TestSearchParams(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(
            SearchParams.__annotations__,
            {
                "page": Optional[int],
                "per_page": Optional[int],
                "sort": Optional[str],
                "sort_dir": Optional[str],
                "filter": Optional[Filter],
            },
        )

    def test_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {"page": None, "expected": 1},
            {"page": "", "expected": 1},
            {"page": "fake", "expected": 1},
            {"page": 0, "expected": 1},
            {"page": -1, "expected": 1},
            {"page": "0", "expected": 1},
            {"page": "-1", "expected": 1},
            {"page": 5.5, "expected": 5},
            {"page": True, "expected": 1},
            {"page": False, "expected": 1},
            {"page": {}, "expected": 1},
            {"page": 1, "expected": 1},
            {"page": 2, "expected": 2},
        ]
        for i in arrange:
            params = SearchParams(page=i["page"])
            self.assertEqual(params.page, i["expected"], i)

    def test_sort_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort)

        arrange = [
            {"sort": None, "expected": None},
            {"sort": "", "expected": None},
            {"sort": "fake", "expected": "fake"},
            {"sort": 0, "expected": "0"},
            {"sort": -1, "expected": "-1"},
            {"sort": "0", "expected": "0"},
            {"sort": "-1", "expected": "-1"},
            {"sort": 5.5, "expected": "5.5"},
            {"sort": True, "expected": "True"},
            {"sort": False, "expected": "False"},
            {"sort": {}, "expected": "{}"},
        ]
        for i in arrange:
            params = SearchParams(sort=i["sort"])
            self.assertEqual(params.sort, i["expected"], i)

    def test_sort_dir_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort=None)
        self.assertIsNone(params.sort_dir)

        arrange = [
            {"sort_dir": None, "expected": "asc"},
            {"sort_dir": "", "expected": "asc"},
            {"sort_dir": "fake", "expected": "asc"},
            {"sort_dir": 0, "expected": "asc"},
            {"sort_dir": {}, "expected": "asc"},
            {"sort_dir": "asc", "expected": "asc"},
            {"sort_dir": "ASC", "expected": "asc"},
            {"sort_dir": "desc", "expected": "desc"},
            {"sort_dir": "DESC", "expected": "desc"},
        ]

        for i in arrange:
            params = SearchParams(sort="name", sort_dir=i["sort_dir"])
            self.assertEqual(params.sort_dir, i["expected"], i)

    def test_filter_prop(self):
        params = SearchParams()
        self.assertIsNone(params.filter)

        arrange = [
            {"filter": None, "expected": None},
            {"filter": "", "expected": None},
            {"filter": "fake", "expected": "fake"},
            {"filter": 0, "expected": "0"},
            {"filter": -1, "expected": "-1"},
            {"filter": "0", "expected": "0"},
            {"filter": "-1", "expected": "-1"},
            {"filter": 5.5, "expected": "5.5"},
            {"filter": True, "expected": "True"},
            {"filter": False, "expected": "False"},
            {"filter": {}, "expected": "{}"},
        ]

        for i in arrange:
            params = SearchParams(filter=i["filter"])
            self.assertEqual(params.filter, i["expected"], i)
