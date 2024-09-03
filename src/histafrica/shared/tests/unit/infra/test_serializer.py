import unittest

from histafrica.shared.infra.django_app.serializers import PaginationSerializer


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
