from datetime import date
import pytest
from unittest.mock import Mock

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.scraper.race_info_scraper import RaceInfoScraper

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
    expected = f"https://www.boatrace.jp/owpc/pc/race/racelist?rno={race}&jcd={stadium:02d}&hd={ymd}"  # noqa
    # actual
    actual = RaceInfoScraper.make_url(d, stadium, race)
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
    mock_html_file = f"racelist.rno={race}&jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.html"  # noqa
    expected_file = f"expected_racelist.rno={race}&jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.json"  # noqa
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = RaceInfoScraper(driver=mock_driver)
    actual = scraper.get(d, stadium, race)
    # assert
    assert actual == expected
