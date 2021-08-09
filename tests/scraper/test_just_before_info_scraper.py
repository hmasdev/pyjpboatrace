from datetime import date
import pytest
from unittest.mock import Mock

from pyjpboatrace.drivers import HTTPGetDriver
from pyjpboatrace.scraper.just_before_info_scraper import (
    JustBeforeInfoScraper,
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
    expected = f"https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno={race}&jcd={stadium:02d}&hd={ymd}"  # noqa
    # actual
    actual = JustBeforeInfoScraper.make_url(d, stadium, race)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "d,stadium,race",
    [
        (
            # usual
            date(2020, 8, 25),
            14,
            7,
        ),
        (
            # racer missing
            date(2020, 11, 29),
            10,
            2,
        ),
        (
            # cancelled race
            date(2019, 1, 26),
            8,
            8,
        ),
    ]
)
def test_get(d: date, stadium: int, race: int):

    # preparation
    mock_html_file = f"beforeinfo.rno={race}&jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.html"  # noqa
    expected_file = f"expected_beforeinfo.rno={race}&jcd={stadium:02d}&hd={d.strftime('%Y%m%d')}.json"  # noqa
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = JustBeforeInfoScraper(driver=mock_driver)
    actual = scraper.get(d, stadium, race)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    "mock_html_file,expected_file",
    [
        (
            # not yet
            "not_yet_beforeinfo.html",
            "expected_not_yet_beforeinfo.json",
        ),
    ]
)
def test_get_for_not_yet(mock_html_file, expected_file):

    # preparation
    d = date.today()
    stadium = 1
    race = 1
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # preprocess
    expected.update(date=d.strftime("%Y-%m-%d"), stadium=stadium, race=race)
    # actual
    scraper = JustBeforeInfoScraper(driver=mock_driver)
    actual = scraper.get(d, stadium, race)
    # assert
    assert actual == expected
