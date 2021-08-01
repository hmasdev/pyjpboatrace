import os
import pytest
import time
from datetime import datetime

from pyjpboatrace.user_information import UserInformation
from pyjpboatrace.drivers import create_chrome_driver, create_firefox_driver
from pyjpboatrace.actions.ibmbraceorjp import deposit, withdraw
from pyjpboatrace.actions.ibmbraceorjp import get_bet_limit, bet
from pyjpboatrace.const import BOATRACE_START, BOATRACE_END

IS_BOATRACE_TIME = BOATRACE_START <= datetime.now().time() <= BOATRACE_END
SECRETSJSON = './.secrets.json'


def get_user_info(secretsjson=SECRETSJSON):
    if os.path.exists(secretsjson):
        return UserInformation(json_file=secretsjson)
    else:
        return None


@pytest.mark.skip(reason='it spends money')
@pytest.mark.skipif(
    not IS_BOATRACE_TIME,
    reason='it is not time for boatrace'
)
@pytest.mark.skipif(
    not os.path.exists(SECRETSJSON),
    reason=f'{SECRETSJSON} not found'
)
@pytest.mark.integrate
@pytest.mark.parametrize(
    'create_driver',
    (
        create_chrome_driver,
        create_firefox_driver,
    )
)
def test_deposit_withdraw(create_driver):
    # preparation
    driver = create_driver()
    user = get_user_info()
    # pre-status
    current = get_bet_limit(driver, user)
    # deposit
    num = 1000
    deposit(num//1000, driver, user)
    time.sleep(10)
    after = get_bet_limit(driver, user)
    assert after == current + num
    # withdraw
    withdraw(driver, user)
    time.sleep(10)
    current = get_bet_limit(driver, user)
    assert current == 0


@pytest.mark.skip(reason='it spends money')
@pytest.mark.skipif(
    not IS_BOATRACE_TIME,
    reason='it is not time for boatrace'
)
@pytest.mark.skipif(
    not os.path.exists(SECRETSJSON),
    reason=f'{SECRETSJSON} not found'
)
@pytest.mark.integrate
@pytest.mark.parametrize(
    'create_driver',
    (
        create_chrome_driver,
        create_firefox_driver,
    )
)
def test_bet(create_driver):
    # preparation
    driver = create_driver()
    user = get_user_info()
    current = get_bet_limit(driver, user)
    if current <= 700:
        # deposit
        num = 1000
        deposit(num//1000, driver, user)
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

    assert bet(
        place=place,
        race=race,
        betdict=betdict,
        driver=driver,
        user=user
    )
