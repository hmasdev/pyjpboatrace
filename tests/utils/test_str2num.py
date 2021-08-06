from pyjpboatrace.utils import str2num


def test_str2num_int():
    # preparation
    input = '1'
    # expected
    expected = 1
    # actual
    actual = str2num(input, int)
    # assert
    assert actual == expected


def test_str2num_float():
    # preparation
    input = '.5'
    # expected
    expected = .5
    # actual
    actual = str2num(input, float)
    # assert
    assert actual == expected


def test_str2num_complex():
    # preparation
    input = '1+1.j'
    # expected
    expected = 1 + 1j
    # actual
    actual = str2num(input, complex)
    # assert
    assert actual == expected


def test_str2num_failure():
    # preparation
    input = '..5'
    # expected
    expected = None
    # actual
    actual = str2num(input, float)
    # assert
    assert actual == expected
