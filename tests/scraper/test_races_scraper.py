from datetime import date
from unittest.mock import Mock

import pytest

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.scraper.races_scraper import RacesScraper

from .._utils import get_expected_json, get_mock_html


@pytest.mark.parametrize(
    "d,stadium",
    [
        (
            date(2021, 1, 1),
            14,
        ),
        (
            date(2021, 12, 1),
            5,
        )
    ]
)
def test_make_url(d: date, stadium: int):
    # preparation
    ymd = d.strftime("%Y%m%d")
    expected = f"https://www.boatrace.jp/owpc/pc/race/raceindex?jcd={stadium:02d}&hd={ymd}"  # noqa
    # actual
    actual = RacesScraper.make_url(d, stadium)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "d,stadium",
    [
        (
            date(2020, 10, 8),
            1,
        ),
    ]
)
def test_get(d: date, stadium: int):

    # preparation
    mock_html_file = f"raceindex.jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.html"  # noqa
    expected_file = f"expected_raceindex.jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.json"  # noqa
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = RacesScraper(driver=mock_driver)
    actual = scraper.get(d, stadium)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "mock_html_file,expected_file",
    [
        (
            "today_raceindex.html",
            "expected_today_raceindex.json"
        ),
    ]
)
def test_get_for_today(mock_html_file, expected_file):

    # preparation
    d = date.today()
    stadium = 1
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # preprocess
    expected.update(date=d.strftime("%Y-%m-%d"), stadium=stadium)
    # actual
    scraper = RacesScraper(driver=mock_driver)
    actual = scraper.get(d, stadium)
    # assert
    assert actual == expected
