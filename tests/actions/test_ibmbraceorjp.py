import os
import unittest
import pytest
import time

from pyjpboatrace.user_information import UserInformation
from pyjpboatrace.drivers import create_chrome_driver
from pyjpboatrace.actions.ibmbraceorjp import deposit, withdraw
from pyjpboatrace.actions.ibmbraceorjp import get_bet_limit, bet


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

    @pytest.mark.skip(reason='it spends money')
    @pytest.mark.skipif(
        not os.path.exists(secretsjson),
        reason=f'{secretsjson} not found'
    )
    def test_bet(self):
        # preparation
        current = get_bet_limit(self.driver, self.user)
        if current <= 700:
            # deposit
            num = 1000
            deposit(num//1000, self.driver, self.user)
            time.sleep(10)

        # bet list
        # TODO automation
        place = 24
        race = 11
        betdict = {
            'trifecta': {'1-2-3': 100},
            'trio': {'2=3=4': 100},
            'exacta': {'2-1': 100},
            'quinella': {'3=4': 100},
            'quinellaplace': {'2=6': 100},
            'win': {'5': 100},
            'placeshow': {'6': 100},
        }

        self.assertTrue(bet(
            place=place,
            race=race,
            betdict=betdict,
            driver=self.driver,
            user=self.user
        ))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest.main()
