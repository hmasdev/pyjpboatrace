import unittest
from pyjpboatrace.utils import str2num


class TestStr2num(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_str2num_int(self):
        # preparation
        input = '1'
        # expected
        expected = 1
        # actual
        actual = str2num(input, int)
        # assert
        self.assertEqual(actual, expected)

    def test_str2num_float(self):
        # preparation
        input = '.5'
        # expected
        expected = .5
        # actual
        actual = str2num(input, float)
        # assert
        self.assertEqual(actual, expected)

    def test_str2num_complex(self):
        # preparation
        input = '1+1.j'
        # expected
        expected = 1 + 1j
        # actual
        actual = str2num(input, complex)
        # assert
        self.assertEqual(actual, expected)

    def test_str2num_failure(self):
        # preparation
        input = '..5'
        # expected
        expected = None
        # actual
        actual = str2num(input, float)
        # assert
        self.assertEqual(actual, expected)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
