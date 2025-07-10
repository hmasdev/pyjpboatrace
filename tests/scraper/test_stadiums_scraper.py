from datetime import date
from unittest.mock import Mock

import pytest

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.scraper.stadiums_scraper import StadiumsScraper

from .._utils import get_expected_json, get_mock_html


@pytest.mark.parametrize(
    "d",
    [
        date(2021, 1, 1),
        date(2021, 12, 1),
    ]
)
def test_make_url(d: date):
    # preparation
    ymd = d.strftime("%Y%m%d")
    expected = f"https://www.boatrace.jp/owpc/pc/race/index?hd={ymd}"
    # actual
    actual = StadiumsScraper.make_url(d)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "d",
    [
        date(2020, 9, 8),
        date(2022, 10, 30),
        date(2025, 4, 7),
        date(2025, 4, 24),
    ]
)
def test_get(d: date):

    # preparation
    mock_html_file = f"index.hd={d.strftime('%Y%m%d')}.html"  # noqa
    expected_file = f"expected_index.hd={d.strftime('%Y%m%d')}.json"  # noqa
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = StadiumsScraper(driver=mock_driver)
    actual = scraper.get(d)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "mock_html_file,expected_file",
    [
        (
            "today_index.html",
            "expected_today_index.json"
        ),
    ]
)
def test_get_for_today(mock_html_file, expected_file):

    # preparation
    d = date.today()
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # preprocess
    expected.update(date=d.strftime("%Y-%m-%d"))
    # actual
    scraper = StadiumsScraper(driver=mock_driver)
    actual = scraper.get(d)
    # assert
    assert actual == expected
