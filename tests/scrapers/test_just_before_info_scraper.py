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
    "mock_html_file,expected_file",
    [
        (
            # usual
            "beforeinfo.rno=7&jcd=14&hd=20200825.html",
            "expected_beforeinfo.rno=7&jcd=14&hd=20200825.json",
        ),
        (
            # racer missing
            "beforeinfo.rno=2&jcd=10&hd=20201129.html",
            "expected_beforeinfo.rno=2&jcd=10&hd=20201129.json",
        ),
        (
            # cancelled race
            "beforeinfo.rno=8&jcd=08&hd=20190126.html",
            "expected_beforeinfo.rno=8&jcd=08&hd=20190126.json",
        ),
        (
            # not yet
            "not_yet_beforeinfo.html",
            "expected_not_yet_beforeinfo.json",
        ),
    ]
)
def test_get(mock_html_file, expected_file):

    # preparation
    expected = get_expected_json(expected_file)
    mock_driver = Mock(HTTPGetDriver)
    mock_driver.page_source = get_mock_html(mock_html_file)
    # actual
    scraper = JustBeforeInfoScraper(driver=mock_driver)
    actual = scraper.get(
        date.today(),  # dummy
        stadium=1,  # dummy
        race=1,  # dummy
    )

    # assert
    assert actual == expected
