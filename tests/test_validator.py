from datetime import date, timedelta

import pytest

from pyjpboatrace.const import NUM_RACES, NUM_STADIUMS
from pyjpboatrace.validator import (
    validate_date,
    validate_race,
    validate_stadium,
)


def test_validate_date_without_value_error():
    validate_date(date.today())
    assert True


def test_validate_date_with_value_error():
    d = date.today() + timedelta(days=1)
    with pytest.raises(ValueError):
        validate_date(d)


def test_validate_stadium_without_value_error():
    for i in range(1, NUM_STADIUMS+1):
        validate_stadium(i)
    assert True


@pytest.mark.parametrize(
    "stadium",
    [
        0,
        NUM_STADIUMS+1,
    ]
)
def test_validate_stadium_with_value_error(stadium: int):
    with pytest.raises(ValueError):
        validate_stadium(stadium)


def test_validate_race_without_value_error():
    for r in range(1, NUM_RACES+1):
        validate_race(r)
    assert True


@pytest.mark.parametrize(
    "race",
    [
        0,
        NUM_RACES+1,
    ]
)
def test_validate_race_with_value_error(race: int):
    with pytest.raises(ValueError):
        validate_race(race)
