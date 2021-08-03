import pytest
from selenium import webdriver
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
from .._driver_fixutures import chrome_driver  # noqa


def test_betting_operator_do_with_no_deposit(chrome_driver):  # noqa

    # argument
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 100}}

    # create state
    depo = 0

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id.return_value = Mock(
        WebElement,
        text=str(depo)
    )

    # preparation
    better = BettingOperator(mock_user, mock_driver)

    # assert
    with pytest.raises(ZeroDepositException):
        better.do(stadium, race, betdict,)


def test_betting_operator_do_with_inactive_stadium(chrome_driver):  # noqa

    # create arguments
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 100}}

    # create state
    depo = 100

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(depo)),
                f"jyo{stadium:02d}": Mock(
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


def test_betting_operator_do_with_inactive_race(chrome_driver):  # noqa

    # create arguments
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 100}}

    # create state
    depo = 100

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.get = Mock()
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(depo)),
                f"jyo{stadium:02d}": Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                f"selRaceNo{race:02d}": Mock(
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


def test_betting_operator_do_with_insufficient_deposit(chrome_driver):  # noqa

    # create arguments
    stadium = 1
    race = 1
    betdict = {"trifecta": {"1-2-3": 500}}

    # create state
    depo = 100

    # create mock
    mock_user = MagicMock(UserInformation)
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(depo)),
                f"jyo{stadium:02d}": Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                f"selRaceNo{race:02d}": Mock(
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


def test_betting_operator_do(chrome_driver):  # noqa

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
    mock_driver = MagicMock(chrome_driver)
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(depo)),
                f"jyo{stadium:02d}": Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                f"selRaceNo{race:02d}": Mock(
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
    args_list = mock_driver.find_element_by_id.call_args_list
    assert "currentBetLimitAmount" == args_list.pop(0)[0][0]
    assert f"jyo{stadium:02d}" == args_list.pop(0)[0][0]
    assert f"selRaceNo{race:02d}" == args_list.pop(0)[0][0]

    bet_list = list(betdict.items())
    while args_list[0][0][0].startswith("betkati"):

        # TODO assert more detailed
        assert args_list.pop(0)[0][0].startswith("betkati")

        bd = bet_list.pop(0)  # bet for kind
        for katishiki in bd[1]:
            for _ in katishiki.replace("=", "-").split("-"):
                # TODO assert more detailed
                assert args_list.pop(0)[0][0].startswith("regbtn")
            assert "amount" == args_list.pop(0)[0][0]
            assert "amount" == args_list.pop(0)[0][0]
            assert "regAmountBtn" == args_list.pop(0)[0][0]

    assert "amount" == args_list.pop(0)[0][0]
    assert "pass" == args_list.pop(0)[0][0]
    assert "submitBet" == args_list.pop(0)[0][0]
    assert "ok" == args_list.pop(0)[0][0]

    # assert for input complete
    # TODO check when find_element_by_class_name is called
    mock_driver.find_element_by_class_name.assert_called_once()
    mock_driver.find_element_by_class_name.assert_called_with("btnSubmit")


@pytest.mark.parametrize(
    "driver_class,is_raised",
    [
        (webdriver.Chrome, False,),
        (webdriver.Firefox, False,),
        (webdriver.Edge, False,),
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
    mock_driver.find_element_by_id = Mock(
        side_effect=create_side_effect(
            {
                "currentBetLimitAmount": Mock(WebElement, text=str(10000)),
                f"jyo{stadium:02d}": Mock(
                    WebElement,
                    get_attribute=Mock(return_value=[])
                ),
                f"selRaceNo{race:02d}": Mock(
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
