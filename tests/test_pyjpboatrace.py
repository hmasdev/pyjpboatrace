import unittest
from unittest import mock
import os
import json
from datetime import date, datetime, timedelta
from logging import getLogger
from pyjpboatrace import PyJPBoatrace

# TODO add test for get function of racer's basic info
# TODO add test for get function of racer's last 3sections info
# TODO add test for get function of racer's season info
# TODO add test for get function of racer's course-wise info


class TestPyjpboatrace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pyjpboatrace = PyJPBoatrace()
        cls.expected_direc = 'tests/data'
        cls.mock_html = 'tests/mock_html'
        cls.logger = getLogger(__name__)

    def setUp(self):
        pass

    def test_get_stadiums(self):

        # preparation
        d = date(2020, 9, 8)
        dstr = d.strftime('%Y%m%d')

        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_index.hd={dstr}.json"
        )
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = self.pyjpboatrace.get_stadiums(d)

        # assertion
        self.assertDictEqual(actual, expected)

    @mock.patch('pyjpboatrace.requestors.Requestor.get')
    def test_get_stadiums_today(self, mock_get):
        # TODAY (=2020/11/30) CASE #
        # preparation
        d = date(2020, 11, 30)
        # set mock
        path = os.path.join(self.mock_html, 'today_index.html')
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8') as f:
            mock_get.return_value = f.read()

        # expectation
        path = os.path.join(self.expected_direc, 'expected_today_index.json')
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = self.pyjpboatrace.get_stadiums(d)

        # assert
        self.assertEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = self.pyjpboatrace.get_12races(d, stadium)

        # assertion
        self.assertDictEqual(actual, expected)

    @mock.patch('pyjpboatrace.requestors.Requestor.get')
    def test_get_12races_today(self, mock_get):
        # TODAY (=2020/12/01) CASE #
        # preparation
        d = date(2020, 12, 1)
        stadium = 1
        # set mock
        path = os.path.join(self.mock_html, 'today_raceindex.html')
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8') as f:
            mock_get.return_value = f.read()

        # expectation
        path = os.path.join(
            self.expected_direc,
            'expected_today_raceindex.json'
        )
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)

        # actual
        actual = self.pyjpboatrace.get_12races(d, stadium)

        # assert
        self.assertEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_race_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_race_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_win_placeshow(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_win_placeshow(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_quinellaplace(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_quinellaplace(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_exacta_quinella(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_exacta_quinella(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_trifecta(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_trifecta(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_odds_trio(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_odds_trio(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_just_before_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_just_before_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @mock.patch('pyjpboatrace.requestors.Requestor.get')
    def test_get_just_before_info_not_yet(self, mock_get):
        # NOT YET DISPLAYED CASE#
        # preparation: anything OK
        d = date(2020, 11, 29)
        stadium = 10
        race = 2
        # set mock
        path = os.path.join(self.mock_html, "not_yet_beforeinfo.html")
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8') as f:
            mock_get.return_value = f.read()
        # expectation
        path = os.path.join(
            self.expected_direc,
            "expected_not_yet_beforeinfo.json"
        )
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_just_before_info(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

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
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual data
        actual = self.pyjpboatrace.get_race_result(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    def test_get_race_result_missing_racer(self):
        # MISSING RACERS CASE #
        # preparation
        d = date(2020, 11, 29)
        dstr = d.strftime('%Y%m%d')
        stadium = 10
        race = 2
        # expectation
        path = os.path.join(
            self.expected_direc,
            f"expected_raceresult.rno={race}&jcd={stadium:02d}&hd={dstr}.json"
        )
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_race_result(d, stadium, race)
        # assertion
        self.assertDictEqual(actual, expected)

    @mock.patch('pyjpboatrace.requestors.Requestor.get')
    def test_get_race_result_not_yet(self, mock_get):
        # NOT YET DISPLAYED CASE#
        # preparation: anything OK
        d = date(2020, 11, 29)
        stadium = 10
        race = 2
        # set mock
        path = os.path.join(self.mock_html, "not_yet_raceresult.html")
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8') as f:
            mock_get.return_value = f.read()
        # expectation
        path = os.path.join(
            self.expected_direc,
            "expected_not_yet_raceresult.json"
        )
        if not os.path.exists(path):
            self.logger.warning(f'{path} not found. Skip it.')
            return None
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = json.load(f)
        # actual
        actual = self.pyjpboatrace.get_race_result(d, stadium, race)
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

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
