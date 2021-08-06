import pytest
import time

from pyjpboatrace.operator import (
    DepositOperator,
    BettingLimitCheckOperator,
    WithdrawOperator,
)

from .._driver_fixutures import chrome_driver  # noqa
from .._utils import is_boatrace_time, get_user_info


@pytest.mark.skipif(
    not is_boatrace_time(),
    reason='it is not time for boatrace'
)
@pytest.mark.skipif(
    get_user_info() is None,
    reason='UserInformation not found'
)
@pytest.mark.integrate
@pytest.mark.spending_money
def test_deposit_withdraw(chrome_driver):  # noqa
    # preparation
    user = get_user_info()
    depositor = DepositOperator(user, chrome_driver)
    betting_limit_checker = BettingLimitCheckOperator(user, chrome_driver)
    withdrawer = WithdrawOperator(user, chrome_driver)
    # pre-status
    current = betting_limit_checker.do()
    # deposit
    num = 1000
    depositor.do(num//1000)
    time.sleep(10)
    after = betting_limit_checker.do()
    assert after == current + num
    # withdraw
    withdrawer.do()
    time.sleep(10)
    current = betting_limit_checker.do()
    assert current == 0
