import unittest
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


class TestPyjpboatrace(unittest.TestCase):

    expected_direc = 'tests/data'
    mock_html = 'tests/mock_html'
    secretsjson = '.secrets.json'

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.secretsjson):
            cls.pyjpboatrace = PyJPBoatrace(
                driver=create_chrome_driver(),
                user_information=UserInformation(json_file=cls.secretsjson)
            )
        else:
            cls.pyjpboatrace = PyJPBoatrace(driver=create_chrome_driver())

    def setUp(self):
        pass

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_stadiums(self):

        # preparation
        d = date(2020, 9, 8)
        dstr = d.strftime('%Y%m%d')

        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_index.hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = self.pyjpboatrace.get_stadiums(d)

        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    @pytest.mark.skipif(
        not os.path.exists(mock_html),
        reason=f'{mock_html} not found'
    )
    @mock.patch('selenium.webdriver.Chrome')
    def test_get_stadiums_today(self, mock_chrome):
        # TODAY (=2020/11/30) CASE #
        # preparation
        d = date(2020, 11, 30)
        # set mock
        path = os.path.join(self.mock_html, 'today_index.html')
        with open(path, 'r', encoding='utf-8') as f:
            mock_chrome.page_source = f.read()

        # expectation
        path = os.path.join(self.expected_direc, 'expected_today_index.json')
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = PyJPBoatrace(driver=mock_chrome).get_stadiums(d)

        # assert
        self.assertEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_12races(self):

        # preparation
        d = date(2020, 10, 8)
        dstr = d.strftime('%Y%m%d')
        stadium = 1

        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_raceindex.jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = self.pyjpboatrace.get_12races(d, stadium)

        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    @pytest.mark.skipif(
        not os.path.exists(mock_html),
        reason=f'{mock_html} not found'
    )
    @mock.patch('selenium.webdriver.Chrome')
    def test_get_12races_today(self, mock_chrome):
        # TODAY (=2020/12/01) CASE #
        # preparation
        d = date(2020, 12, 1)
        stadium = 1
        # set mock
        path = os.path.join(self.mock_html, 'today_raceindex.html')
        with open(path, 'r', encoding='utf-8') as f:
            mock_chrome.page_source = f.read()

        # expectation
        path = os.path.join(
            self.expected_direc,
            'expected_today_raceindex.json'
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = PyJPBoatrace(driver=mock_chrome).get_12races(d, stadium)

        # assert
        self.assertEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_race_info(self):

        # USUAL CASE #
        # preparation
        d = date(2020, 10, 24)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 1
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_racelist.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_race_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_race_info_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_racelist.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_race_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_win_placeshow(self):
        # USUAL CASE #
        # preparation
        d = date(2020, 10, 24)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 1
        # load true data
        path = os.path.join(
            self.expected_direc,
            f"expected_oddstf.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_win_placeshow(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_win_placeshow_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_oddstf.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_win_placeshow(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    def test_get_odds_win_placeshow_cancelled_race(self):
        # CANCELLED RACERS CASE #
        # preparation
        d = date(2019, 1, 26)
        stadium = 8
        race = 8
        # expectation
        expected = {'win': {}, 'place_show': {}}
        # actual
        actual = self.pyjpboatrace.get_odds_win_placeshow(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_quinellaplace(self):
        # USUAL CASE #
        # preparation
        d = date(2020, 10, 24)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 1
        # load true data
        path = os.path.join(
            self.expected_direc,
            f"expected_oddsk.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_quinellaplace(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_quinellaplace_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_oddsk.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_quinellaplace(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    def test_get_odds_quinellaplace_cancelled_race(self):
        # CANCELLED RACE CASE #
        # preparation
        d = date(2019, 1, 26)
        stadium = 8
        race = 8
        # load true data
        expected = {}
        # actual data
        actual = self.pyjpboatrace.get_odds_quinellaplace(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_exacta_quinella(self):
        # USUAL CASE #
        # preparation
        d = date(2020, 10, 24)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 1
        # load true data
        path = os.path.join(
            self.expected_direc,
            f"expected_odds2tf.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_exacta_quinella(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_exacta_quinella_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_odds2tf.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_exacta_quinella(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    def test_get_odds_exacta_quinella_cancelled_race(self):
        # CANCELLED RACE CASE #
        # preparation
        d = date(2019, 1, 26)
        stadium = 8
        race = 8
        # load true data
        expected = {'exacta': {}, 'quinella': {}}
        # actual data
        actual = self.pyjpboatrace.get_odds_exacta_quinella(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_trifecta(self):
        # USUAL CASE #
        # preparation
        d = date(2020, 10, 24)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 1
        # load true data
        path = os.path.join(
            self.expected_direc,
            f"expected_odds3t.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_trifecta(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_trifecta_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_odds3t.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_trifecta(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    def test_get_odds_trifecta_cancelled_race(self):
        # CANCELLED RACERS CASE #
        # preparation
        d = date(2019, 1, 26)
        stadium = 8
        race = 8
        # expectation
        expected = {}
        # actual
        actual = self.pyjpboatrace.get_odds_trifecta(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_trio(self):
        # USUAL CASE #
        # preparation
        d = date(2020, 10, 24)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 1
        # load true data
        path = os.path.join(
            self.expected_direc,
            f"expected_odds3f.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_trio(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_odds_trio_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_odds3f.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_trio(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    def test_get_odds_trio_cancelled_race(self):
        # CANCELLED RACERS CASE #
        # preparation
        d = date(2019, 1, 26)
        stadium = 8
        race = 8
        # expectation
        expected = {}
        # actual
        actual = self.pyjpboatrace.get_odds_trio(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_just_before_info(self):
        # USUAL CASE #
        # preparation
        d = date(2020, 8, 25)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 7
        # load true data
        path = os.path.join(
            self.expected_direc,
            f"expected_beforeinfo.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_just_before_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_just_before_info_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_beforeinfo.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_just_before_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    @pytest.mark.skipif(
        not os.path.exists(mock_html),
        reason=f'{mock_html} not found'
    )
    @mock.patch('selenium.webdriver.Chrome')
    def test_get_just_before_info_not_yet(self, mock_chrome):
        # NOT YET DISPLAYED CASE#
        # preparation: anything OK
        d = date(2020, 11, 29)
        stadium = 10
        race = 2
        # set mock
        path = os.path.join(self.mock_html, "not_yet_beforeinfo.html")
        with open(path, 'r', encoding='utf-8') as f:
            mock_chrome.page_source = f.read()

        # expectation
        path = os.path.join(
            self.expected_direc,
            "expected_not_yet_beforeinfo.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        pyjpboatrace = PyJPBoatrace(driver=mock_chrome)
        actual = pyjpboatrace.get_just_before_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_just_before_info_cancelled_race(self):
        # CANCELLED RACERS CASE #
        # preparation
        d = date(2019, 1, 26)
        dstr = d.strftime('%Y%m%d')
        stadium = 8
        race = 8
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_beforeinfo.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_just_before_info(d, stadium, race)
        # assertion
        # self.assertDictEqual(actual, expected)
        assert actual == expected

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_race_result(self):
        # USUAL CASE #
        # preparation
        d = date(2020, 10, 24)
        dstr = d.strftime('%Y%m%d')
        stadium = 14
        race = 1
        # load true data
        path = os.path.join(
            self.expected_direc,
            f"expected_raceresult.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_race_result(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_get_race_result_missing_racer(self):
        # MISSING RACERS CASE #

        for d, std, race in [
            (date(2020, 11, 29), 10, 2),
            (date(2018, 1, 1), 21, 3),
            (date(2013, 9, 22), 1, 10),
        ]:
            # TODO use pytest.mark.parametrize
            # ref. https://github.com/pytest-dev/pytest/issues/541

            # preparation
            dstr = d.strftime('%Y%m%d')
            # expectation
            path = os.path.join(
                self.expected_direc,
                f"expected_raceresult.rno={race}&jcd={std:02d}&hd={dstr}.json"
            )
            with open(path, 'r', encoding='utf-8-sig') as f:
                expected = json.load(f)
            # actual
            actual = self.pyjpboatrace.get_race_result(d, std, race)
            # assertion
            assert actual == expected

    def test_get_race_result_cancelled_race(self):
        # CANCELLED RACERS CASE #
        # preparation
        d = date(2019, 1, 26)
        stadium = 8
        race = 8
        # expectation
        expected = {}
        # actual
        actual = self.pyjpboatrace.get_race_result(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    @pytest.mark.skipif(
        not os.path.exists(mock_html),
        reason=f'{mock_html} not found'
    )
    @mock.patch('selenium.webdriver.Chrome')
    def test_get_race_result_not_yet(self, mock_chrome):
        # NOT YET DISPLAYED CASE#
        # preparation: anything OK
        d = date(2020, 11, 29)
        stadium = 10
        race = 2
        # set mock
        path = os.path.join(self.mock_html, "not_yet_raceresult.html")
        with open(path, 'r', encoding='utf-8') as f:
            mock_chrome.page_source = f.read()

        # expectation
        path = os.path.join(
            self.expected_direc,
            "expected_not_yet_raceresult.json"
        )
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        pyjpboatrace = PyJPBoatrace(driver=mock_chrome)
        actual = pyjpboatrace.get_race_result(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    def test_get_race_result_invalid_arguments(self):

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
        msg = f'Date d must be before today. {d} is given.'
        with self.assertRaises(ValueError, msg=msg):
            self.pyjpboatrace.get_race_result(d, stadium, race)

        # invalid stadium
        d = datetime.today().date()
        stadium = 0
        race = 2
        msg = f'Stadium must be between 1 and 24. {stadium} is given.'
        with self.assertRaises(ValueError, msg=msg):
            self.pyjpboatrace.get_race_result(d, stadium, race)

        # invalid race
        d = datetime.today().date()
        stadium = 10
        race = 13
        msg = f'Race must be between 1 and 12. {race} is given.'
        with self.assertRaises(ValueError, msg=msg):
            self.pyjpboatrace.get_race_result(d, stadium, race)

    @pytest.mark.skipif(
        not IS_BOATRACE_TIME,
        reason='it is not time for boatrace'
    )
    @pytest.mark.skipif(
        not os.path.exists(secretsjson),
        reason=f'{secretsjson} not found'
    )
    def test_deposit_withdraw(self):
        # pre-status
        current = self.pyjpboatrace.get_bet_limit()
        # deposit
        num = 1000
        self.pyjpboatrace.deposit(num//1000)
        time.sleep(10)
        after = self.pyjpboatrace.get_bet_limit()
        self.assertEqual(after, current+num)
        # withdraw
        self.pyjpboatrace.withdraw()
        time.sleep(10)
        current = self.pyjpboatrace.get_bet_limit()
        self.assertEqual(current, 0)

    @pytest.mark.skip(reason='it spends money')
    @pytest.mark.skipif(
        not IS_BOATRACE_TIME,
        reason='it is not time for boatrace'
    )
    @pytest.mark.skipif(
        not os.path.exists(secretsjson),
        reason=f'{secretsjson} not found'
    )
    def test_bet(self):
        # preparation
        current = self.pyjpboatrace.get_bet_limit()
        if current <= 700:
            # deposit
            num = 1000
            self.pyjpboatrace.deposit(num//1000)
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

        self.assertTrue(self.pyjpboatrace.bet(
            place=place,
            race=race,
            trifecta_betting_dict=betdict['trifecta'],
            trio_betting_dict=betdict['trio'],
            exacta_betting_dict=betdict['exacta'],
            quinella_betting_dict=betdict['quinella'],
            quinellaplace_betting_dict=betdict['quinellaplace'],
            win_betting_dict=betdict['win'],
            placeshow_betting_dict=betdict['placeshow']
        ))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.pyjpboatrace.close()


if __name__ == "__main__":
    unittest.main()
