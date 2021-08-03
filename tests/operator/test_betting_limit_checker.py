import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from unittest.mock import MagicMock, Mock

from pyjpboatrace.exceptions import UnableActionException
from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.operator.betting_limit_checker import (
    BettingLimitCheckOperator,
)
from pyjpboatrace.user_information import UserInformation

from .._utils import create_side_effect
from .._driver_fixutures import chrome_driver  # noqa


@pytest.mark.parametrize(
    "depo",
    [
        "0",
        "100",
        "1,000",
        "1,000,000",
    ]
)
def test_betting_limit_check_operator_do(depo, chrome_driver):  # noqa

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(depo)),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    betting_limit_checker = BettingLimitCheckOperator(
        mock_user,
        mock_driver,
    )

    # execute
    actual = betting_limit_checker.do()

    # assert
    assert actual == int(depo.replace(",", ""))
    mock_driver.find_element_by_id.assert_called_once_with(
        'currentBetLimitAmount'
    )


@pytest.mark.parametrize(
    "driver_class,is_raised",
    [
        (webdriver.Chrome, False,),
        (webdriver.Firefox, False,),
        (webdriver.Edge, False,),
        (HTTPGetDriver, True,),
    ]
)
def test_betting_limit_check_operator_for_driver(driver_class, is_raised):

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(driver_class)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(10000)),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    betting_limit_checker = BettingLimitCheckOperator(
        mock_user,
        mock_driver,
    )

    # execute
    if is_raised:
        with pytest.raises(UnableActionException):
            betting_limit_checker.do()
    else:
        betting_limit_checker.do()
