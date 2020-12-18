import os
import unittest
import pytest
import time

from pyjpboatrace.user_information import UserInformation
from pyjpboatrace.drivers import create_chrome_driver
from pyjpboatrace.actions.ibmbraceorjp import get_bet_limit, deposit, withdraw


class TestIbmbraceorjp(unittest.TestCase):

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
    def test_deposit_withdraw(self):
        # pre-status
        current = get_bet_limit(self.driver, self.user)
        # deposit
        num = 1000
        deposit(num//1000, self.driver, self.user)
        time.sleep(10)
        after = get_bet_limit(self.driver, self.user)
        self.assertEqual(after, current+num)
        # withdraw
        withdraw(self.driver, self.user)
        time.sleep(10)
        current = get_bet_limit(self.driver, self.user)
        self.assertEqual(current, 0)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main()
