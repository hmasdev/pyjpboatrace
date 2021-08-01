from unittest import mock
import pytest
import os
import json
import time
from datetime import date, datetime, timedelta
from pyjpboatrace import PyJPBoatrace
from pyjpboatrace.user_information import UserInformation
from pyjpboatrace.drivers import create_chrome_driver
from pyjpboatrace.const import BOATRACE_START, BOATRACE_END

# TODO add test for get function of racer's basic info
# TODO add test for get function of racer's last 3sections info
# TODO add test for get function of racer's season info
# TODO add test for get function of racer's course-wise info

IS_BOATRACE_TIME = BOATRACE_START <= datetime.now().time() <= BOATRACE_END
EXPECTED_DIREC = 'tests/data'
MOCK_HTML_DIREC = 'tests/mock_html'
SECRETSJSON = '.secrets.json'


@pytest.fixture(scope='module')
def pyjpboatrace_(secretsjson=SECRETSJSON):
    if os.path.exists(secretsjson):
        user = UserInformation(json_file=secretsjson)
    else:
        user = None
    driver = create_chrome_driver()
    pyjpboatrace = PyJPBoatrace(driver=driver, user_information=user)
    yield pyjpboatrace
    pyjpboatrace.close()


def get_expected(header, **options):
    name = '.'.join([
        header,
        '&'.join([f'{k}={v}' for k, v in options.items()]),
        'json',
    ]).replace('..', '.')
    path = os.path.join(EXPECTED_DIREC, name)
    with open(path, 'r', encoding='utf-8-sig') as f:
        expected = json.load(f)
    return expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_stadiums(pyjpboatrace_):
    # preparation
    d = date(2020, 9, 8)
    dstr = d.strftime('%Y%m%d')
    # expectation
    expected = get_expected('expected_index', hd=dstr)
    # actual
    actual = pyjpboatrace_.get_stadiums(d)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.skipif(
    not os.path.exists(MOCK_HTML_DIREC),
    reason=f'{MOCK_HTML_DIREC} not found'
)
@mock.patch('selenium.webdriver.Chrome')
def test_get_stadiums_today(mock_chrome):
    # TODAY (=2020/11/30) CASE #
    # preparation
    d = date(2020, 11, 30)
    # set mock
    path = os.path.join(MOCK_HTML_DIREC, 'today_index.html')
    with open(path, 'r', encoding='utf-8') as f:
        mock_chrome.page_source = f.read()

    # expectation
    expected = get_expected('expected_today_index')

    # actual
    actual = PyJPBoatrace(driver=mock_chrome).get_stadiums(d)

    # assert
    assert actual == expected

    # close
    mock_chrome.close()


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_12races(pyjpboatrace_):

    # preparation
    d = date(2020, 10, 8)
    dstr = d.strftime('%Y%m%d')
    stadium = 1

    # expectation
    expected = get_expected(
        "expected_raceindex",
        jcd=f"{stadium:02d}",
        hd=dstr,
    )

    # actual
    actual = pyjpboatrace_.get_12races(d, stadium)

    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.skipif(
    not os.path.exists(MOCK_HTML_DIREC),
    reason=f'{MOCK_HTML_DIREC} not found'
)
@mock.patch('selenium.webdriver.Chrome')
def test_get_12races_today(mock_chrome):
    # TODAY (=2020/12/01) CASE #
    # preparation
    d = date(2020, 12, 1)
    stadium = 1
    # set mock
    path = os.path.join(MOCK_HTML_DIREC, 'today_raceindex.html')
    with open(path, 'r', encoding='utf-8') as f:
        mock_chrome.page_source = f.read()

    # expectation
    expected = get_expected('expected_today_raceindex')

    # actual
    actual = PyJPBoatrace(driver=mock_chrome).get_12races(d, stadium)

    # assert
    assert actual == expected

    # close
    mock_chrome.close()


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_race_info(pyjpboatrace_):

    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # expectation
    expected = get_expected(
        'expected_racelist',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual
    actual = pyjpboatrace_.get_race_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_race_info_missing_racer(pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected(
        'expected_racelist',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual
    actual = pyjpboatrace_.get_race_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_win_placeshow(pyjpboatrace_):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected(
        'expected_oddstf',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_odds_win_placeshow(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_win_placeshow_missing_racer(pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected(
        'expected_oddstf',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual
    actual = pyjpboatrace_.get_odds_win_placeshow(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_win_placeshow_cancelled_race(pyjpboatrace_):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # expectation
    expected = {'win': {}, 'place_show': {}}
    # actual
    actual = pyjpboatrace_.get_odds_win_placeshow(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_quinellaplace(pyjpboatrace_):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected(
        'expected_oddsk',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_odds_quinellaplace(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_quinellaplace_missing_racer(pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected(
        'expected_oddsk',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_odds_quinellaplace(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_quinellaplace_cancelled_race(pyjpboatrace_):
    # CANCELLED RACE CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # load true data
    expected = {}
    # actual data
    actual = pyjpboatrace_.get_odds_quinellaplace(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_exacta_quinella(pyjpboatrace_):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected(
        'expected_odds2tf',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_odds_exacta_quinella(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_exacta_quinella_missing_racer(pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected(
        'expected_odds2tf',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_odds_exacta_quinella(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_exacta_quinella_cancelled_race(pyjpboatrace_):
    # CANCELLED RACE CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # load true data
    expected = {'exacta': {}, 'quinella': {}}
    # actual data
    actual = pyjpboatrace_.get_odds_exacta_quinella(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_trifecta(pyjpboatrace_):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected(
        'expected_odds3t',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )

    # actual data
    actual = pyjpboatrace_.get_odds_trifecta(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_trifecta_missing_racer(pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # load true data
    expected = get_expected(
        'expected_odds3t',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_odds_trifecta(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_trifecta_cancelled_race(pyjpboatrace_):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # expectation
    expected = {}
    # actual
    actual = pyjpboatrace_.get_odds_trifecta(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_trio(pyjpboatrace_):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected(
        'expected_odds3f',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_odds_trio(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_odds_trio_missing_racer(pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected(
        'expected_odds3f',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual
    actual = pyjpboatrace_.get_odds_trio(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_odds_trio_cancelled_race(pyjpboatrace_):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # expectation
    expected = {}
    # actual
    actual = pyjpboatrace_.get_odds_trio(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_just_before_info(pyjpboatrace_):
    # USUAL CASE #
    # preparation
    d = date(2020, 8, 25)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 7
    # load true data
    expected = get_expected(
        'expected_beforeinfo',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_just_before_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_just_before_info_missing_racer(pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    d = date(2020, 11, 29)
    dstr = d.strftime('%Y%m%d')
    stadium = 10
    race = 2
    # expectation
    expected = get_expected(
        'expected_beforeinfo',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual
    actual = pyjpboatrace_.get_just_before_info(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.skipif(
    not os.path.exists(MOCK_HTML_DIREC),
    reason=f'{MOCK_HTML_DIREC} not found'
)
@mock.patch('selenium.webdriver.Chrome')
def test_get_just_before_info_not_yet(mock_chrome):
    # NOT YET DISPLAYED CASE#
    # preparation: anything OK
    d = date(2020, 11, 29)
    stadium = 10
    race = 2
    # set mock
    path = os.path.join(MOCK_HTML_DIREC, "not_yet_beforeinfo.html")
    with open(path, 'r', encoding='utf-8') as f:
        mock_chrome.page_source = f.read()

    # expectation
    expected = get_expected("expected_not_yet_beforeinfo")
    # actual
    pyjpboatrace = PyJPBoatrace(driver=mock_chrome)
    actual = pyjpboatrace.get_just_before_info(d, stadium, race)
    # assertion
    assert actual == expected
    # close
    mock_chrome.close()


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_just_before_info_cancelled_race(pyjpboatrace_):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    dstr = d.strftime('%Y%m%d')
    stadium = 8
    race = 8
    # expectation
    expected = get_expected(
        'expected_beforeinfo',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual
    actual = pyjpboatrace_.get_just_before_info(d, stadium, race)
    # assertion
    # assert actual == expected
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
def test_get_race_result(pyjpboatrace_):
    # USUAL CASE #
    # preparation
    d = date(2020, 10, 24)
    dstr = d.strftime('%Y%m%d')
    stadium = 14
    race = 1
    # load true data
    expected = get_expected(
        'expected_raceresult',
        rno=race,
        jcd=f"{stadium:02d}",
        hd=dstr,
    )
    # actual data
    actual = pyjpboatrace_.get_race_result(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.integrate
@pytest.mark.parametrize(
    "d,std,race",
    [
        (date(2020, 11, 29), 10, 2),
        (date(2018, 1, 1), 21, 3),
        (date(2013, 9, 22), 1, 10),
    ]
)
def test_get_race_result_missing_racer(d, std, race, pyjpboatrace_):
    # MISSING RACERS CASE #
    # preparation
    dstr = d.strftime('%Y%m%d')
    # expectation
    expected = get_expected(
        'expected_raceresult',
        rno=race,
        jcd=f"{std:02d}",
        hd=dstr,
    )
    # actual
    actual = pyjpboatrace_.get_race_result(d, std, race)
    # assertion
    assert actual == expected


@pytest.mark.integrate
def test_get_race_result_cancelled_race(pyjpboatrace_):
    # CANCELLED RACERS CASE #
    # preparation
    d = date(2019, 1, 26)
    stadium = 8
    race = 8
    # expectation
    expected = {}
    # actual
    actual = pyjpboatrace_.get_race_result(d, stadium, race)
    # assertion
    assert actual == expected


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.skipif(
    not os.path.exists(MOCK_HTML_DIREC),
    reason=f'{MOCK_HTML_DIREC} not found'
)
@mock.patch('selenium.webdriver.Chrome')
def test_get_race_result_not_yet(mock_chrome):
    # NOT YET DISPLAYED CASE#
    # preparation: anything OK
    d = date(2020, 11, 29)
    stadium = 10
    race = 2
    # set mock
    path = os.path.join(MOCK_HTML_DIREC, "not_yet_raceresult.html")
    with open(path, 'r', encoding='utf-8') as f:
        mock_chrome.page_source = f.read()

    # expectation
    expected = get_expected('expected_not_yet_raceresult')
    # actual
    pyjpboatrace = PyJPBoatrace(driver=mock_chrome)
    actual = pyjpboatrace.get_race_result(d, stadium, race)
    # assertion
    assert actual == expected
    # close
    mock_chrome.close()


@pytest.mark.integrate
def test_get_race_result_invalid_arguments(pyjpboatrace_):

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
        pyjpboatrace_.get_race_result(d, stadium, race)

    # invalid stadium
    d = datetime.today().date()
    stadium = 0
    race = 2
    # msg = f'Stadium must be between 1 and 24. {stadium} is given.'
    with pytest.raises(ValueError):
        pyjpboatrace_.get_race_result(d, stadium, race)

    # invalid race
    d = datetime.today().date()
    stadium = 10
    race = 13
    # msg = f'Race must be between 1 and 12. {race} is given.'
    with pytest.raises(ValueError):
        pyjpboatrace_.get_race_result(d, stadium, race)


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
def test_deposit_withdraw(pyjpboatrace_):
    # pre-status
    current = pyjpboatrace_.get_bet_limit()
    # deposit
    num = 1000
    pyjpboatrace_.deposit(num//1000)
    time.sleep(10)
    after = pyjpboatrace_.get_bet_limit()
    assert after == current+num
    # withdraw
    pyjpboatrace_.withdraw()
    time.sleep(10)
    current = pyjpboatrace_.get_bet_limit()
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
def test_bet(pyjpboatrace_):
    # preparation
    current = pyjpboatrace_.get_bet_limit()
    if current <= 700:
        # deposit
        num = 1000
        pyjpboatrace_.deposit(num//1000)
        time.sleep(10)

    # bet list
    # TODO automation
    place = 19
    race = 12
    betdict = {
        'trifecta': {'1-2-4': 100},
        'trio': {'2=3=4': 100},
        'exacta': {'2-1': 100},
        'quinella': {'3=4': 100},
        'quinellaplace': {'2=6': 100},
        'win': {'5': 100},
        'placeshow': {'6': 100},
    }

    assert pyjpboatrace_.bet(
        place=place,
        race=race,
        trifecta_betting_dict=betdict['trifecta'],
        trio_betting_dict=betdict['trio'],
        exacta_betting_dict=betdict['exacta'],
        quinella_betting_dict=betdict['quinella'],
        quinellaplace_betting_dict=betdict['quinellaplace'],
        win_betting_dict=betdict['win'],
        placeshow_betting_dict=betdict['placeshow']
    )
