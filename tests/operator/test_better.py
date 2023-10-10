import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from unittest.mock import MagicMock, Mock

from pyjpboatrace.exceptions import (
    ZeroDepositException,
    InactiveRace,
    InactiveStadium,
    InsufficientDepositException,
    UnableActionException,
)
from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.operator.better import BettingOperator
from pyjpboatrace.user_information import UserInformation

from .._utils import create_side_effect


def test_betting_operator_do_with_no_deposit():

    # argument
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 100}}

    # create state
    depo = 0

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(webdriver.Chrome)
    mock_driver.find_element.return_value = Mock(
        WebElement,
        text=str(depo)
    )

    # preparation
    better = BettingOperator(mock_user, mock_driver)

    # assert
    with pytest.raises(ZeroDepositException):
        better.do(stadium, race, betdict,)


def test_betting_operator_do_with_inactive_stadium():

    # create arguments
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 100}}

    # create state
    depo = 100

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(webdriver.Chrome)
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(depo)),  # noqa
                (By.ID, f"jyo{stadium:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=["borderNone", ])
                ),
            }
        )
    )

    # preparation
    better = BettingOperator(mock_user, mock_driver)

    # assert
    with pytest.raises(InactiveStadium):
        better.do(stadium, race, betdict)


def test_betting_operator_do_with_inactive_race():

    # create arguments
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 100}}

    # create state
    depo = 100

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(webdriver.Chrome)
    mock_driver.get = Mock()
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(depo)),  # noqa
                (By.ID, f"jyo{stadium:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                (By.ID, f"selRaceNo{race:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=["end", ])
                ),
            }
        )
    )

    # preparation
    better = BettingOperator(mock_user, mock_driver)

    # assert
    with pytest.raises(InactiveRace):
        better.do(stadium, race, betdict)


def test_betting_operator_do_with_insufficient_deposit():

    # create arguments
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 500}}

    # create state
    depo = 100

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(webdriver.Chrome)
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(depo)),  # noqa
                (By.ID, f"jyo{stadium:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                (By.ID, f"selRaceNo{race:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    better = BettingOperator(mock_user, mock_driver)

    # assert
    with pytest.raises(InsufficientDepositException):
        better.do(stadium, race, betdict)


def test_betting_operator_do():

    # create arguments
    stadium = 1
    race = 1
    betdict = {
        "win": {"1": 1000},
        "placeshow": {"1": 100, "2": 100},
        "exacta": {"1-2": 100},
        "quinella": {"1=2": 100, "1=3": 100},
        "quinellaplace":  {"1=2": 100},
        "trifecta": {"1-2-3": 500},
        "trio": {"1=2=3": 500, "2=3=4": 500},
    }  # Order is critical... FIXME

    # create state
    depo = 100000

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(webdriver.Chrome)
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(depo)),  # noqa
                (By.ID, f"jyo{stadium:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                (By.ID, f"selRaceNo{race:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    better = BettingOperator(mock_user, mock_driver)

    # execute
    better.do(stadium, race, betdict)

    # assert
    args_list = mock_driver.find_element.call_args_list
    logging.debug(args_list)
    assert (By.ID, "currentBetLimitAmount") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, "currentBetLimitAmount") == args_list.pop(0)[0]
    assert (By.ID, f"jyo{stadium:02d}") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, f"jyo{stadium:02d}") == args_list.pop(0)[0]
    assert (By.ID, f"selRaceNo{race:02d}") == args_list.pop(0)[0]  # NOTE: WebDriverWait.until context  # noqa
    assert (By.ID, f"selRaceNo{race:02d}") == args_list.pop(0)[0]

    bet_list = list(betdict.items())
    while args_list[0][0][1].startswith("betkati"):

        # TODO assert more detailed
        assert args_list.pop(0)[0][1].startswith("betkati")

        bd = bet_list.pop(0)  # bet for kind
        for katishiki in bd[1]:
            for _ in katishiki.replace("=", "-").split("-"):
                # TODO assert more detailed
                assert args_list.pop(0)[0][1].startswith("regbtn")
            assert (By.ID, "amount") == args_list.pop(0)[0]
            assert (By.ID, "amount") == args_list.pop(0)[0]
            assert (By.ID, "regAmountBtn") == args_list.pop(0)[0]

    # assert for input complete
    # TODO check when find_element_by_class_name is called
    assert (By.CLASS_NAME, "btnSubmit") == args_list.pop(0)[0]
    assert (By.ID, "amount") == args_list.pop(0)[0]
    assert (By.ID, "pass") == args_list.pop(0)[0]
    assert (By.ID, "submitBet") == args_list.pop(0)[0]
    assert (By.ID, "ok") == args_list.pop(0)[0]


@pytest.mark.parametrize(
    "driver_class,is_raised",
    [
        (webdriver.Chrome, False,),
        (webdriver.Firefox, False,),
        # (webdriver.Edge, False,),
        (HTTPGetDriver, True,),
    ]
)
def test_betting_operator_for_driver(driver_class, is_raised):

    # create arguments
    stadium = 1
    race = 1
    betdict = {
        "win": {"1": 1000},
        "placeshow": {"1": 100, "2": 100},
        "exacta": {"1-2": 100},
        "quinella": {"1=2": 100, "1=3": 100},
        "quinellaplace":  {"1=2": 100},
        "trifecta": {"1-2-3": 500},
        "trio": {"1=2=3": 500, "2=3=4": 500},
    }  # Order is critical... FIXME

    # create mock
    mock_user = MagicMock(UserInformation, vote_pass=None)
    mock_driver = MagicMock(driver_class)
    mock_driver.find_element = Mock(
        side_effect=create_side_effect(
            {
                (By.ID, "currentBetLimitAmount"): Mock(WebElement, text=str(10000)),  # noqa
                (By.ID, f"jyo{stadium:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                (By.ID, f"selRaceNo{race:02d}"): Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
            },
            default_value=Mock(WebElement),
        )
    )

    # preparation
    better = BettingOperator(mock_user, mock_driver)

    # execute
    if is_raised:
        with pytest.raises(UnableActionException):
            better.do(stadium, race, betdict)
    else:
        better.do(stadium, race, betdict)
