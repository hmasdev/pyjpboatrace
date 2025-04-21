import os

import pytest
from selenium.common.exceptions import WebDriverException

from ._driver_fixutures import driver  # noqa

EXPECTED_DIREC = 'tests/data'


@pytest.mark.integrate
def test_driver_get(driver):  # noqa
    # preparation
    url = 'https://example.com'
    # expected
    path = os.path.join(EXPECTED_DIREC, "expected_example.com.html")
    with open(path, 'r', encoding='utf-8-sig') as f:
        expected = f.read()
    expected = ''.join(expected.split())\
                 .replace("<!doctypehtml>", '')\
                 .replace("/>", '>')
    # actual
    driver.get(url)
    actual = driver.page_source
    actual = ''.join(actual.split())\
               .replace("<!doctypehtml>", '')\
               .replace("/>", '>')
    # assert
    assert actual == expected


@pytest.mark.integrate
def test_driver_get_404_not_found(driver):  # noqa
    # preparation
    url = 'https://this_does_not_exists_hogehogehogehoge'
    # test
    with pytest.raises(WebDriverException):
        driver.get(url)
