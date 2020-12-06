import unittest
import pytest
import os
import json
from logging import getLogger
from pyjpboatrace.requestors import BoatracejpRequestor

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

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
