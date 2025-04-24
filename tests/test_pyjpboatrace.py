import re
import time
from datetime import date, datetime, timedelta
from typing import Any, Dict
from unittest import mock

import pytest

from pyjpboatrace import PyJPBoatrace
from pyjpboatrace.const import STADIUMS_MAP
from pyjpboatrace.exceptions import NoDataException, RaceCancelledException

from ._driver_fixutures import chrome_driver  # noqa
from ._utils import (
    get_expected_json,
    get_mock_html,
    get_user_info,
    is_boatrace_time,
)

# TODO add test for get function of racer's basic info
# TODO add test for get function of racer's last 3sections info
# TODO add test for get function of racer's season info
# TODO add test for get function of racer's course-wise info


@pytest.fixture(scope='module')
def boatrace_tools(chrome_driver) -> PyJPBoatrace:  # type: ignore  # noqa
    user = get_user_info()
    pyjpboatrace = PyJPBoatrace(
        driver=chrome_driver,
        user_information=user,
        close_driver_when_closing_pyjpboatrace=False,
        # because closing driver in pytest.fixture
    )
    yield pyjpboatrace
    pyjpboatrace.close()


@pytest.mark.integrate
@pytest.mark.parametrize(
    "d",
    [
        date(2020, 9, 8),
        date(2022, 10, 30),
    ]
)
def test_get_stadiums(d: date, boatrace_tools: PyJPBoatrace):
    # preparation
    dstr = d.strftime('%Y%m%d')
    # expectation
    expected = get_expected_json(f"expected_index.hd={dstr}.json")
    # actual
    actual = boatrace_tools.get_stadiums(d)
    # assertion
    assert actual == expected


@mock.patch('selenium.webdriver.Chrome')
def test_get_stadiums_today(mock_chrome):
    # TODAY (=2020/11/30) CASE #
    # preparation
    d = date(2020, 11, 30)
    # set mock
    mock_chrome.page_source = get_mock_html("today_index.html")

    # expectation
    expected = get_expected_json('expected_today_index.json')
    expected.update(date=d.strftime("%Y-%m-%d"))

    # actual
    actual = PyJPBoatrace(driver=mock_chrome).get_stadiums(d)

    # assert
    assert actual == expected

    # close
    mock_chrome.close()


@pytest.mark.integrate
def test_get_12races(boatrace_tools: PyJPBoatrace):

    # preparation
    d = date(2020, 10, 8)
    dstr = d.strftime('%Y%m%d')
    stadium = 1

    # expectation
    expected = get_expected_json(
        f"expected_raceindex.jcd={stadium:02d}&hd={dstr}.json",
    )

    # actual
    actual = boatrace_tools.get_12races(d, stadium)

    # assertion
    assert actual == expected


@mock.patch('selenium.webdriver.Chrome')
def test_get_12races_today(mock_chrome):
    # TODAY (=2020/12/01) CASE #
    # preparation
    d = date(2020, 12, 1)
    stadium = 1
    # set mock
    mock_chrome.page_source = get_mock_html("today_raceindex.html")

    # expectation
    expected = get_expected_json('expected_today_raceindex.json')
    expected.update(date=d.strftime("%Y-%m-%d"), stadium=stadium)

    # actual
    actual = PyJPBoatrace(driver=mock_chrome).get_12races(d, stadium)

    # assert
    assert actual == expected

    # close
    mock_chrome.close()


@pytest.mark.integrate
def test_get_race_info(boatrace_tools: PyJPBoatrace):

    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # expectation
    expected = get_expected_json(
        f'expected_racelist.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_race_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_race_info_missing_racer(boatrace_tools: PyJPBoatrace):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected_json(
        f'expected_racelist.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_race_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_win_placeshow(boatrace_tools: PyJPBoatrace):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected_json(
        f'expected_oddstf.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_odds_win_placeshow(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_win_placeshow_missing_racer(boatrace_tools: PyJPBoatrace):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected_json(
        f'expected_oddstf.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_odds_win_placeshow(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_win_placeshow_cancelled_race(boatrace_tools: PyJPBoatrace):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # actual
    with pytest.raises(RaceCancelledException):
        boatrace_tools.get_odds_win_placeshow(d, stadium, race)


@pytest.mark.integrate
def test_get_odds_quinellaplace(boatrace_tools: PyJPBoatrace):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected_json(
        f'expected_oddsk.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_odds_quinellaplace(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_quinellaplace_missing_racer(boatrace_tools: PyJPBoatrace):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected_json(
        f'expected_oddsk.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_odds_quinellaplace(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_quinellaplace_cancelled_race(boatrace_tools: PyJPBoatrace):
    # CANCELLED RACE CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # assert
    with pytest.raises(RaceCancelledException):
        boatrace_tools.get_odds_quinellaplace(d, stadium, race)


@pytest.mark.integrate
def test_get_odds_exacta_quinella(boatrace_tools: PyJPBoatrace):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected_json(
        f'expected_odds2tf.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_odds_exacta_quinella(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_exacta_quinella_missing_racer(boatrace_tools: PyJPBoatrace):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected_json(
        f'expected_odds2tf.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_odds_exacta_quinella(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_exacta_quinella_cancelled_race(boatrace_tools: PyJPBoatrace):
    # CANCELLED RACE CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # assert
    with pytest.raises(RaceCancelledException):
        boatrace_tools.get_odds_exacta_quinella(d, stadium, race)


@pytest.mark.integrate
def test_get_odds_trifecta(boatrace_tools: PyJPBoatrace):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected_json(
        f'expected_odds3t.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )

    # actual data
    actual = boatrace_tools.get_odds_trifecta(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_trifecta_missing_racer(boatrace_tools: PyJPBoatrace):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # load true data
    expected = get_expected_json(
        f'expected_odds3t.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_odds_trifecta(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_trifecta_cancelled_race(boatrace_tools: PyJPBoatrace):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # assert
    with pytest.raises(RaceCancelledException):
        boatrace_tools.get_odds_trifecta(d, stadium, race)


@pytest.mark.integrate
def test_get_odds_trio(boatrace_tools: PyJPBoatrace):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected_json(
        f'expected_odds3f.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_odds_trio(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
@pytest.mark.skipif(
    not is_boatrace_time(),
    reason='it is not time for boatrace'
)
@pytest.mark.parametrize(
    "method_name",
    [
        "get_odds_trifecta",
        "get_odds_trio",
        "get_odds_exacta_quinella",
        "get_odds_quinellaplace",
        "get_odds_win_placeshow",
    ]
)
def test_get_real_time_odds(method_name: str, boatrace_tools: PyJPBoatrace):

    # preparation
    today = date.today()
    stadiums = boatrace_tools.get_stadiums(today)

    # search active race
    for stadium_str, dic in stadiums.items():
        if stadium_str not in (s for _, s in STADIUMS_MAP):
            continue
        if "R以降発売中" in dic["status"]:
            race = dic["next_race"]
            stadium = {k: v for v, k in STADIUMS_MAP}.get(stadium_str)
            break
    else:
        raise Exception("Failed to find any active race.")

    # actual data
    actual: Dict[str, Any]
    actual = boatrace_tools.__getattribute__(method_name)(today, stadium, race)
    # assertion
    assert actual.get("date") == today.strftime("%Y-%m-%d")
    assert actual.get("stadium") == stadium
    assert actual.get("race") == race
    assert re.fullmatch(r"(\d|\d\d):\d\d", actual.get("update"))  # type: ignore  # noqa


@pytest.mark.integrate
def test_get_odds_trio_missing_racer(boatrace_tools: PyJPBoatrace):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected_json(
        f'expected_odds3f.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_odds_trio(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_trio_cancelled_race(boatrace_tools: PyJPBoatrace):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # assert
    with pytest.raises(RaceCancelledException):
        boatrace_tools.get_odds_trio(d, stadium, race)


@pytest.mark.integrate
def test_get_just_before_info(boatrace_tools: PyJPBoatrace):
    # USUAL CASE #
    # preparation
    d = date(2020, 8, 25)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 7
    # load true data
    expected = get_expected_json(
        f'expected_beforeinfo.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_just_before_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_just_before_info_missing_racer(boatrace_tools: PyJPBoatrace):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected_json(
        f'expected_beforeinfo.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_just_before_info(d, stadium, race)
    # assertion
    assert actual == expected


@mock.patch('selenium.webdriver.Chrome')
def test_get_just_before_info_not_yet(mock_chrome):
    # NOT YET DISPLAYED CASE#
    # preparation: anything OK
    d = date(2020, 11, 29)
    stadium = 10
    race = 2
    # set mock
    mock_chrome.page_source = get_mock_html("not_yet_beforeinfo.html")

    # expectation
    expected = get_expected_json("expected_not_yet_beforeinfo.json")
    expected.update(date=d.strftime("%Y-%m-%d"), stadium=stadium, race=race)
    # actual
    pyjpboatrace = PyJPBoatrace(driver=mock_chrome)
    actual = pyjpboatrace.get_just_before_info(d, stadium, race)
    # assertion
    assert actual == expected
    # close
    mock_chrome.close()


@pytest.mark.integrate
def test_get_just_before_info_cancelled_race(boatrace_tools: PyJPBoatrace):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    dstr = d.strftime('%Y%m%d')
    stadium = 8
    race = 8
    # expectation
    expected = get_expected_json(
        f'expected_beforeinfo.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_just_before_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_race_result(boatrace_tools: PyJPBoatrace):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected_json(
        f'expected_raceresult.rno={race}&jcd={stadium:02d}&hd={dstr}.json',
    )
    # actual data
    actual = boatrace_tools.get_race_result(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
@pytest.mark.parametrize(
    "d,std,race",
    [
        (date(2020, 11, 29), 10, 2),
        (date(2018, 1, 1), 21, 3),
        # NOTE: https://boatrace.jp/owpc/pc/race/raceresult?rno=10&jcd=01&hd=20130922 has not responsed data since 2023/10/08.  # noqa
        # (date(2013, 9, 22), 1, 10),
    ]
)
def test_get_race_result_missing_racer(d, std, race, boatrace_tools):
    # MISSING RACERS CASE #
    # preparation
    dstr = d.strftime('%Y%m%d')
    # expectation
    expected = get_expected_json(
        f'expected_raceresult.rno={race}&jcd={std:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_race_result(d, std, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
@pytest.mark.parametrize(
    "d,std,race",
    [
        (date(2019, 4, 8), 11, 5),
        (date(2021, 6, 14), 12, 1),
        (date(2021, 1, 3), 14, 10),
    ]
)
def test_get_race_result_for_tie_case(d, std, race, boatrace_tools):
    # MISSING RACERS CASE #
    # preparation
    dstr = d.strftime('%Y%m%d')
    # expectation
    expected = get_expected_json(
        f'expected_raceresult.rno={race}&jcd={std:02d}&hd={dstr}.json',
    )
    # actual
    actual = boatrace_tools.get_race_result(d, std, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_race_result_cancelled_race(boatrace_tools: PyJPBoatrace):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # assert
    with pytest.raises(RaceCancelledException):
        boatrace_tools.get_race_result(d, stadium, race)


@mock.patch('selenium.webdriver.Chrome')
def test_get_race_result_not_yet(mock_chrome):
    # NOT YET DISPLAYED CASE#
    # preparation: anything OK
    d = date(2020, 11, 29)
    stadium = 10
    race = 2
    # set mock
    mock_chrome.page_source = get_mock_html("not_yet_raceresult.html")

    # assert
    pyjpboatrace = PyJPBoatrace(driver=mock_chrome)
    with pytest.raises(NoDataException):
        pyjpboatrace.get_race_result(d, stadium, race)

    # close
    mock_chrome.close()


@pytest.mark.integrate
def test_get_race_result_invalid_arguments(boatrace_tools: PyJPBoatrace):

    # TODO invalid args test for get_stadiums
    # TODO invalid args test for get_12races
    # TODO invalid args test for get_just_before_info
    # TODO invalid args test for get_race_info
    # TODO invalid args test for get_odds_win_placeshow
    # TODO invalid args test for get_odds_quinellaplace
    # TODO invalid args test for get_odds_exacta_quinella
    # TODO invalid args test for get_odds_trifecta
    # TODO invalid args test for get_odds_trio

    # invalid date
    d = (datetime.today()+timedelta(days=1)).date()
    stadium = 10
    race = 2
    # msg = f'Date d must be before today. {d} is given.'
    with pytest.raises(ValueError):
        boatrace_tools.get_race_result(d, stadium, race)

    # invalid stadium
    d = datetime.today().date()
    stadium = 0
    race = 2
    # msg = f'Stadium must be between 1 and 24. {stadium} is given.'
    with pytest.raises(ValueError):
        boatrace_tools.get_race_result(d, stadium, race)

    # invalid race
    d = datetime.today().date()
    stadium = 10
    race = 13
    # msg = f'Race must be between 1 and 12. {race} is given.'
    with pytest.raises(ValueError):
        boatrace_tools.get_race_result(d, stadium, race)


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
def test_deposit_withdraw(boatrace_tools: PyJPBoatrace):
    # pre-status
    current = boatrace_tools.get_bet_limit()
    # deposit
    num = 1000
    boatrace_tools.deposit(num//1000)
    time.sleep(10)
    after = boatrace_tools.get_bet_limit()
    assert after == current+num
    # withdraw
    boatrace_tools.withdraw()
    time.sleep(10)
    current = boatrace_tools.get_bet_limit()
    assert current == 0


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
def test_bet(boatrace_tools: PyJPBoatrace):
    # preparation
    current = boatrace_tools.get_bet_limit()
    if current <= 700:
        # deposit
        num = 1000
        boatrace_tools.deposit(num//1000)
        time.sleep(10)

    # scrape stadiums/races
    stadiums_dic = boatrace_tools.get_stadiums(date.today())

    _flag = False
    for key in stadiums_dic:
        stadium = {s: i for i, s in STADIUMS_MAP}[key]
        races_dic = boatrace_tools.get_12races(date.today(), stadium)
        for r, dic in races_dic.items():
            if dic.get("status") == "投票":
                race = int(r[:-1])
                _flag = True
                break
        if _flag:
            break
        time.sleep(2)

    if not _flag:
        raise Exception("Failed to find any active races.")

    # bet list
    betdict = {
        'trifecta': {'1-2-4': 100},
        'trio': {'2=3=4': 100},
        'exacta': {'2-1': 100},
        'quinella': {'3=4': 100},
        'quinellaplace': {'2=6': 100},
        'win': {'5': 100},
        'placeshow': {'6': 100},
    }

    assert boatrace_tools.bet(
        stadium=stadium,
        race=race,
        trifecta_betting_dict=betdict['trifecta'],
        trio_betting_dict=betdict['trio'],
        exacta_betting_dict=betdict['exacta'],
        quinella_betting_dict=betdict['quinella'],
        quinellaplace_betting_dict=betdict['quinellaplace'],
        win_betting_dict=betdict['win'],
        placeshow_betting_dict=betdict['placeshow']
    )
