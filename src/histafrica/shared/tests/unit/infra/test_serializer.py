import unittest

from rest_framework import serializers

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


class StubCollectionSerialer(CollectionSerializer):
    child = StubSerializer()
