import unittest
import pytest
import os
from selenium.common.exceptions import WebDriverException

from pyjpboatrace.drivers import create_chrome_driver
from pyjpboatrace.drivers import create_firefox_driver
from pyjpboatrace.drivers import create_edge_driver
from pyjpboatrace.drivers import create_httpget_driver


class TestChromeDriver(unittest.TestCase):

    expected_direc = 'tests/data'

    @classmethod
    def setUpClass(cls):
        cls.driver = create_chrome_driver()

    def setUp(self):
        pass

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_driver_get(self):
        # preparation
        url = 'https://example.com'
        # expected
        path = os.path.join(self.expected_direc, "expected_example.com.html")
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = f.read()
        # actual
        self.driver.get(url)
        actual = self.driver.page_source
        # assert
        self.assertEqual(
            ''.join(actual.split()),
            ''.join(expected.split())
              .replace("<!doctypehtml>", '')
              .replace("/>", '>'),
        )

    def test_driver_get_404_not_found(self):
        url = 'https://this_does_not_exists_hogehogehogehoge'
        with self.assertRaises(WebDriverException):
            self.driver.get(url)

    def tearDown(self):
        pass

    @ classmethod
    def tearDownClass(cls):
        cls.driver.close()


class TestFirefoxDriver(unittest.TestCase):

    expected_direc = 'tests/data'

    @classmethod
    def setUpClass(cls):
        cls.driver = create_firefox_driver()

    def setUp(self):
        pass

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_driver_get(self):
        # preparation
        url = 'https://example.com'
        # expected
        path = os.path.join(self.expected_direc, "expected_example.com.html")
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = f.read()
        # actual
        self.driver.get(url)
        actual = self.driver.page_source
        # assert
        self.assertEqual(
            ''.join(actual.split()),
            ''.join(expected.split())
              .replace("<!doctypehtml>", '')
              .replace("/>", '>'),
        )

    def test_driver_get_404_not_found(self):
        url = 'https://this_does_not_exists_hogehogehogehoge'
        with self.assertRaises(WebDriverException):
            self.driver.get(url)

    def tearDown(self):
        pass

    @ classmethod
    def tearDownClass(cls):
        cls.driver.close()


class TestEdgeDriver(unittest.TestCase):

    expected_direc = 'tests/data'

    @classmethod
    def setUpClass(cls):
        cls.driver = create_edge_driver()

    def setUp(self):
        pass

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_driver_get(self):
        # preparation
        url = 'https://example.com'
        # expected
        path = os.path.join(self.expected_direc, "expected_example.com.html")
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = f.read()
        # actual
        self.driver.get(url)
        actual = self.driver.page_source
        # assert
        self.assertEqual(
            ''.join(actual.split()),
            ''.join(expected.split()).replace(
                "<!doctypehtml>", '').replace("/>", '>'),
        )

    def test_driver_get_404_not_found(self):
        url = 'https://this_does_not_exists_hogehogehogehoge'
        with self.assertRaises(WebDriverException):
            self.driver.get(url)

    def tearDown(self):
        pass

    @ classmethod
    def tearDownClass(cls):
        cls.driver.close()


class TestHTTPGetDriver(unittest.TestCase):

    expected_direc = 'tests/data'

    @classmethod
    def setUpClass(cls):
        cls.driver = create_httpget_driver()

    def setUp(self):
        pass

    @pytest.mark.skipif(
        not os.path.exists(expected_direc),
        reason=f'{expected_direc} not found'
    )
    def test_driver_get(self):
        # preparation
        url = 'https://example.com'
        # expected
        path = os.path.join(self.expected_direc, "expected_example.com.html")
        with open(path, 'r', encoding='utf-8-sig') as f:
            expected = f.read()
        # actual
        self.driver.get(url)
        actual = self.driver.page_source
        # assert
        self.assertEqual(
            ''.join(actual.split()),
            ''.join(expected.split()),
        )

    def test_driver_get_404_not_found(self):
        url = 'https://this_does_not_exists_hogehogehogehoge'
        with self.assertRaises(WebDriverException):
            self.driver.get(url)

    def tearDown(self):
        pass

    @ classmethod
    def tearDownClass(cls):
        cls.driver.close()


if __name__ == "__main__":
    unittest.main()
