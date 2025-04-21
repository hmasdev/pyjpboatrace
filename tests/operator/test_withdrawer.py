import logging
from unittest.mock import MagicMock, Mock

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.exceptions import UnableActionException, ZeroDepositException
from pyjpboatrace.operator.withdrawer import WithdrawOperator
from pyjpboatrace.user_information import UserInformation

from .._utils import create_side_effect


def test_withdraw_operator_do():

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass='dummy')
    mock_driver = MagicMock(webdriver.Chrome)
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(100)),  # noqa
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    withdrawer = WithdrawOperator(mock_user, mock_driver)

    # execute
    withdrawer.do()

    # assert
    args_list = mock_driver.find_element.call_args_list
    logging.debug(args_list)
    assert (By.ID, "currentBetLimitAmount") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, "currentBetLimitAmount") == args_list.pop(0)[0]
    assert (By.ID, "gnavi01") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, "gnavi01") == args_list.pop(0)[0]
    assert (By.ID, "account") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, "account") == args_list.pop(0)[0]
    assert (By.ID, "accountBetPassword") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, "accountBetPassword") == args_list.pop(0)[0]
    assert (By.ID, "executeAccount") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, "executeAccount") == args_list.pop(0)[0]
    assert (By.ID, "ok") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, "ok") == args_list.pop(0)[0]
    assert not args_list


def test_withdraw_oprator_do_without_deposit():

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass='dummy')
    mock_driver = MagicMock(webdriver.Chrome)
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(0)),  # noqa
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
        # (webdriver.Edge, False,),
        (HTTPGetDriver, True,),
    ]
)
def test_withdraw_operator_do_for_driver(driver_class, is_raised):

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(driver_class)
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(100)),  # noqa
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
