import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from unittest.mock import MagicMock, Mock

from pyjpboatrace.exceptions import UnableActionException
from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.operator.depositor import DepositOperator
from pyjpboatrace.user_information import UserInformation

from .._driver_fixutures import chrome_driver  # noqa


def test_deposit_operator_do(chrome_driver):  # noqa

    # create arguments
    depo_amt_unit_thousands_yen = 5

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id = Mock(
        return_value=Mock(WebElement)
    )

    # preparation
    depositor = DepositOperator(mock_user, mock_driver)

    # execute
    depositor.do(depo_amt_unit_thousands_yen)

    # assert
    args_list = mock_driver.find_element_by_id.call_args_list

    assert "gnavi01" == args_list.pop(0)[0][0]
    assert "charge" == args_list.pop(0)[0][0]
    assert "chargeInstructAmt" == args_list.pop(0)[0][0]
    assert "chargeBetPassword" == args_list.pop(0)[0][0]
    assert "executeCharge" == args_list.pop(0)[0][0]
    assert "ok" == args_list.pop(0)[0][0]
    assert not args_list


@pytest.mark.parametrize(
    "driver_class,is_raised",
    [
        (webdriver.Chrome, False,),
        (webdriver.Firefox, False,),
        (webdriver.Edge, False,),
        (HTTPGetDriver, True,),
    ]
)
def test_deposit_operator_do_for_driver(driver_class, is_raised):
    # create arguments
    depo_amt_unit_thousands_yen = 5

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(driver_class)
    mock_driver.find_element_by_id = Mock(
        return_value=Mock(WebElement)
    )

    # preparation
    depositor = DepositOperator(mock_user, mock_driver)

    # execute
    if is_raised:
        with pytest.raises(UnableActionException):
            depositor.do(depo_amt_unit_thousands_yen)
    else:
        depositor.do(depo_amt_unit_thousands_yen)
