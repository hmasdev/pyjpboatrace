import pytest
import time
from pyjpboatrace.operator import (
    DepositOperator,
    BettingOperator,
    BettingLimitCheckOperator,
)

from .._driver_fixutures import chrome_driver  # noqa
from .._utils import is_boatrace_time, get_user_info


@pytest.mark.skip(reason="Duplicate with test_bet in test_pyjpboatrace.py")
@pytest.mark.skip(reason='it spends money')
@pytest.mark.skipif(
    not is_boatrace_time(),
    reason='it is not time for boatrace'
)
@pytest.mark.skipif(
    get_user_info() is None,
    reason='UserInformation not found',
)
@pytest.mark.integrate
def test_bet(chrome_driver):  # noqa
    # preparation
    user = get_user_info()
    betting_limit_checker = BettingLimitCheckOperator(user, chrome_driver)
    depositor = DepositOperator(user, chrome_driver)
    better = BettingOperator(user, chrome_driver)

    current = betting_limit_checker.do()
    if current <= 700:
        # deposit
        num = 1000
        depositor.do(num//1000)
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

    assert better.do(
        place=place,
        race=race,
        betdict=betdict,
    )
