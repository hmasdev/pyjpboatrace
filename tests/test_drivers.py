import pytest
import os
from selenium.common.exceptions import WebDriverException

from pyjpboatrace.drivers import create_chrome_driver
from pyjpboatrace.drivers import create_firefox_driver
# from pyjpboatrace.drivers import create_edge_driver  # TODO test edge driver
from pyjpboatrace.drivers import create_httpget_driver

EXPECTED_DIREC = 'tests/data'


@pytest.mark.skipif(
    not os.path.exists(EXPECTED_DIREC),
    reason=f'{EXPECTED_DIREC} not found'
)
@pytest.mark.parametrize(
    'create_driver',
    (
        create_chrome_driver,
        create_firefox_driver,
        # create_edge_driver,
        create_httpget_driver,
    )
)
def test_driver_get(create_driver):
    # preparation
    url = 'https://example.com'
    driver = create_driver()
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
    # quit
    driver.close()


@pytest.mark.parametrize(
    'create_driver',
    (
        create_chrome_driver,
        create_firefox_driver,
        # create_edge_driver,
        create_httpget_driver,
    )
)
def test_driver_get_404_not_found(create_driver):
    # preparation
    driver = create_driver()
    url = 'https://this_does_not_exists_hogehogehogehoge'
    # test
    with pytest.raises(WebDriverException):
        driver.get(url)
    # quit
    driver.close()
