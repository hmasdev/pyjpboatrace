from datetime import date
from unittest.mock import Mock

import pytest

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.exceptions import RaceCancelledException
from pyjpboatrace.scraper.trio_odds_scraper import (
    TrioOddsScraper,
)

from .._utils import get_expected_json, get_mock_html


@pytest.mark.parametrize(
    "d,stadium,race",
    [
        (
            date(2021, 1, 1),
            14,
            1,
        ),
        (
            date(2021, 12, 1),
            5,
            12
        )
    ]
)
def test_make_url(d: date, stadium: int, race: int):
    # preparation
    ymd = d.strftime("%Y%m%d")
    expected = f"https://www.boatrace.jp/owpc/pc/race/odds3f?rno={race}&jcd={stadium:02d}&hd={ymd}"  # noqa
    # actual
    actual = TrioOddsScraper.make_url(d, stadium, race)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "d,stadium,race",
    [
        (
            # usual
            date(2020, 10, 24),
            14,
            1,
        ),
        (
            # racer missing
            date(2020, 11, 29),
            10,
            2,
        ),
    ]
)
def test_get(d: date, stadium: int, race: int):

    # preparation
    mock_html_file = f"odds3f.rno={race}&jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.html"  # noqa
    expected_file = f"expected_odds3f.rno={race}&jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.json"  # noqa
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = TrioOddsScraper(driver=mock_driver)
    actual = scraper.get(d, stadium, race)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "d,stadium,race",
    [
        (
            date(2019, 1, 26),
            8,
            8,
        ),
    ]
)
def test_get_for_cancelled_race(d: date, stadium: int, race: int):
    # preparation
    mock_html_file = f"odds3f.rno={race}&jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.html"  # noqa
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    scraper = TrioOddsScraper(driver=mock_driver)
    # assert
    with pytest.raises(RaceCancelledException):
        scraper.get(d, stadium, race)


@pytest.mark.parametrize(
    "mock_html_file,expected_file",
    [
        (
            "realtime_odds3f.html",
            "expected_realtime_odds3f.json",
        ),
    ]
)
def test_get_for_race_before_timelimit(mock_html_file: str, expected_file: str):  # noqa
    # preparation
    d = date.today()
    stadium = 1
    race = 1
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    expected = get_expected_json(expected_file)
    # preprocess
    expected.update(date=d.strftime("%Y-%m-%d"), stadium=stadium, race=race)
    # actual
    scraper = TrioOddsScraper(driver=mock_driver)
    actual = scraper.get(d, stadium, race)
    # assert
    assert actual == expected
