import unittest

from rest_framework import serializers

from histafrica.shared.application.dto import PaginationOutput
from histafrica.shared.infra.django_app.serializers import (
    CollectionSerializer,
    PaginationSerializer,
    ResourceSerializer,
)


class TestPaginationSerializer(unittest.TestCase):

    def test_serialize(self):
        pagination = {
            "current_page": "1",
            "per_page": "2",
            "last_page": "3",
            "total": "4",
        }

        data = PaginationSerializer(instance=pagination).data

        self.assertEqual(
            data, {"current_page": 1, "per_page": 2, "last_page": 3, "total": 4}
        )


class StubSerializer(ResourceSerializer):
    name = serializers.CharField()


class StubCollectionSerializer(CollectionSerializer):
    child = StubSerializer()


class TestCollectionSerializer(unittest.TestCase):

    def test_if_throw_an_error_when_instance_is_not_pagination_output(self):
        error_message = "instance must be a PaginationOutput"
        with self.assertRaises(TypeError) as assert_error:
            CollectionSerializer()
        self.assertEqual(str(assert_error.exception), error_message)

        with self.assertRaises(TypeError) as assert_error:
            CollectionSerializer(instance={})
        self.assertEqual(str(assert_error.exception), error_message)

        with self.assertRaises(TypeError) as assert_error:
            CollectionSerializer(instance=1)
        self.assertEqual(str(assert_error.exception), error_message)

    def test__init__(self):
        pagination = PaginationOutput(
            items=[1, 2, 3, 4], current_page=1, per_page=2, last_page=3, total=4
        )
        collection = StubCollectionSerializer(instance=pagination)
        self.assertEqual(collection.pagination, pagination)
