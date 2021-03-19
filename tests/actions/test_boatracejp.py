import os
import unittest
import pytest
from pyjpboatrace.user_information import UserInformation
from pyjpboatrace.drivers import create_chrome_driver, create_firefox_driver
from pyjpboatrace.actions.boatracejp import login, check_login_status, logout
from pyjpboatrace.exceptions import LoginFailException


class TestBoatracejpWithChrome(unittest.TestCase):

    secretsjson = './.secrets.json'

    @classmethod
    def setUpClass(cls):
        cls.driver = create_chrome_driver()
        if os.path.exists(cls.secretsjson):
            cls.user = UserInformation(json_file=cls.secretsjson)
        else:
            cls.user = None

    def setUp(self):
        pass

    @pytest.mark.skipif(
        not os.path.exists(secretsjson),
        reason=f'{secretsjson} not found'
    )
    def test_login_logout(self):
        # pre-status
        self.assertFalse(check_login_status(self.driver))
        # login
        self.assertTrue(login(self.driver, self.user))
        self.assertTrue(check_login_status(self.driver))
        # logout
        self.assertTrue(logout(self.driver))
        self.assertFalse(check_login_status(self.driver))

    def test_login_wrong_pass(self):
        # preparation
        user = UserInformation('a', 'b', 'c', 'd')
        # pre-status
        self.assertFalse(check_login_status(self.driver))
        # login
        with self.assertRaises(LoginFailException):
            login(self.driver, user)
        self.assertFalse(check_login_status(self.driver))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


class TestBoatracejpWithFirefox(unittest.TestCase):

    secretsjson = './.secrets.json'

    @classmethod
    def setUpClass(cls):
        cls.driver = create_firefox_driver()
        if os.path.exists(cls.secretsjson):
            cls.user = UserInformation(json_file=cls.secretsjson)
        else:
            cls.user = None

    def setUp(self):
        pass

    @pytest.mark.skipif(
        not os.path.exists(secretsjson),
        reason=f'{secretsjson} not found'
    )
    def test_login_logout(self):
        # pre-status
        self.assertFalse(check_login_status(self.driver))
        # login
        self.assertTrue(login(self.driver, self.user))
        self.assertTrue(check_login_status(self.driver))
        # logout
        self.assertTrue(logout(self.driver))
        self.assertFalse(check_login_status(self.driver))

    def test_login_wrong_pass(self):
        # preparation
        user = UserInformation('a', 'b', 'c', 'd')
        # pre-status
        self.assertFalse(check_login_status(self.driver))
        # login
        with self.assertRaises(LoginFailException):
            login(self.driver, user)
        self.assertFalse(check_login_status(self.driver))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main()
