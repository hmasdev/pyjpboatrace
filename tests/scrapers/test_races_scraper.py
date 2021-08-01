from datetime import date
import pytest
from unittest.mock import Mock

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.scraper.races_scraper import RacesScraper

from .utils import get_expected_json, get_mock_html


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
    "mock_html_file,expected_file",
    [
        (
            "today_raceindex.html",
            "expected_today_raceindex.json"
        ),
        (
            "raceindex.jcd=01&hd=20201008.html",
            "expected_raceindex.jcd=01&hd=20201008.json",
        )
    ]
)
def test_get(mock_html_file, expected_file):

    # preparation
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = RacesScraper(driver=mock_driver)
    actual = scraper.get(
        date.today(),  # dummy
        stadium=1,  # dummy
    )

    # assert
    assert actual == expected
