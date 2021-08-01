from datetime import date
import pytest
from unittest.mock import Mock

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.scraper.stadiums_scraper import StadiumsScraper

from .utils import get_expected_json, get_mock_html


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
    "mock_html_file,expected_file",
    [
        (
            "today_index.html",
            "expected_today_index.json"
        ),
        (
            "index.hd=20200908.html",
            "expected_index.hd=20200908.json",
        )
    ]
)
def test_get(mock_html_file, expected_file):

    # preparation
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = StadiumsScraper(driver=mock_driver)
    actual = scraper.get(
        date.today(),  # dummy
    )

    # assert
    assert actual == expected
