import unittest
import pytest
import os
import json
from logging import getLogger
from requests.exceptions import ConnectionError
from pyjpboatrace.requestors import BoatracejpRequestor
from pyjpboatrace.exceptions import LoginFailException

_login_info_file = './.secrets.json'
_login_info_not_found = not os.path.exists(_login_info_file)


class TestRequestorWithLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expected_direc = 'tests/data'
        cls.logger = getLogger(__name__)

        cls.__login_info = None
        if not _login_info_not_found:
            with open(_login_info_file, 'r', encoding='utf-8-sig') as f:
                cls.__login_info = json.load(f)

        try:
            cls.requestor = BoatracejpRequestor(**cls.__login_info)
        except LoginFailException:
            cls.requestor = None

    def setUp(self):
        pass

    @pytest.mark.skipif(_login_info_not_found, reason="login info not found")
    def test_create_requestor_valid_id_pass(self):
        # create
        requestor = BoatracejpRequestor(**self.__login_info)
        # check
        self.assertTrue(requestor.check_login_status())

        # create
        requestor2 = BoatracejpRequestor(login_info_json=_login_info_file)
        # check
        self.assertTrue(requestor2.check_login_status())

    def test_create_requestor_invalid_id_pass(self):
        # create
        with self.assertRaises(LoginFailException):
            BoatracejpRequestor(
                userid='invalid',
                pin='invalid',
                auth_pass='invalid',
                vote_pass='invalid',
            )

    @pytest.mark.skipif(_login_info_not_found, reason="login info not found")
    def test_requestor_get(self):
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
        actual = self.requestor.get(url).text
        # assert
        self.assertEqual(actual, expected)

    @pytest.mark.skipif(_login_info_not_found, reason="login info not found")
    def test_requestor_get_404notfound(self):
        url = 'https://this_does_not_exists_hogehogehogehoge'
        with self.assertRaises(ConnectionError):
            self.requestor.get(url)

    @pytest.mark.skipif(_login_info_not_found, reason="login info not found")
    def test_requestor_post(self):
        # preparation
        url = 'https://httpbin.org/post'
        expected = {'val': '1', 'name': 'First Last'}
        # actual
        response = self.requestor.post(url, data=expected)
        actual = json.loads(response.text)
        # assert
        self.assertDictEqual(actual['form'], expected)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
