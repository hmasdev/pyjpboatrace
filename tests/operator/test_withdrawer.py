import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from unittest.mock import MagicMock, Mock

from pyjpboatrace.exceptions import UnableActionException, ZeroDepositException
from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.operator.withdrawer import WithdrawOperator
from pyjpboatrace.user_information import UserInformation

from .._utils import create_side_effect
from .._driver_fixutures import chrome_driver  # noqa


def test_withdraw_operator_do(chrome_driver):  # noqa

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(100)),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    withdrawer = WithdrawOperator(mock_user, mock_driver)

    # execute
    withdrawer.do()

    # assert
    args_list = mock_driver.find_element_by_id.call_args_list

    assert "currentBetLimitAmount" == args_list.pop(0)[0][0]
    assert "gnavi01" == args_list.pop(0)[0][0]
    assert "account" == args_list.pop(0)[0][0]
    assert "accountBetPassword" == args_list.pop(0)[0][0]
    assert "executeAccount" == args_list.pop(0)[0][0]
    assert "ok" == args_list.pop(0)[0][0]
    assert not args_list


def test_withdraw_oprator_do_without_deposit(chrome_driver):  # noqa

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(0)),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    withdrawer = WithdrawOperator(mock_user, mock_driver)

    # assert
    with pytest.raises(ZeroDepositException):
        withdrawer.do()


@pytest.mark.parametrize(
    "driver_class,is_raised",
    [
        (webdriver.Chrome, False,),
        (webdriver.Firefox, False,),
        (webdriver.Edge, False,),
        (HTTPGetDriver, True,),
    ]
)
def test_withdraw_operator_do_for_driver(driver_class, is_raised):  # noqa

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(driver_class)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(100)),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    withdrawer = WithdrawOperator(mock_user, mock_driver)

    # execute
    if is_raised:
        with pytest.raises(UnableActionException):
            withdrawer.do()
    else:
        withdrawer.do()
