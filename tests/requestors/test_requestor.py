import unittest
import os
from logging import getLogger
from pyjpboatrace.requestors import Requestor
from requests.exceptions import ConnectionError


class TestRequestor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_direc = 'tests/data'
        cls.requestor = Requestor()
        cls.logger = getLogger(__name__)

    def setUp(self):
        pass

    def test_requestor(self):
        # preparation
        url = 'https://example.com'
        # expected
        path = os.path.join(self.expected_direc, "expected_example.com.html")
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = f.read()
        # actual
        actual = self.requestor.get(url)
        # assert
        self.assertEqual(actual, expected)

    def test_requestor_404notfound(self):
        url = 'https://this_does_not_exists_hogehogehogehoge'
        with self.assertRaises(ConnectionError):
            self.requestor.get(url)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
