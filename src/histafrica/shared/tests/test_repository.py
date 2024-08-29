import unittest

from histafrica.shared.domain.repository import RepositoryInterface


class TestRepositoryInterface(unittest.TestCase):

    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface with abstract "
            + "methods delete, find_all, find_by_id, insert, update",
        )
