from datetime import date

from .const import NUM_RACES, NUM_STADIUMS


def validate_date(d: date):
    """Validate date.

    Args:
        d (date)

    Raises:
        ValueError: Occurred when d >= {date.today()}
    """
    if d > date.today():
        raise ValueError(f"Date must be <= today. But {d} is given.")


def validate_stadium(stadium: int):
    """Validate stadium ID

    Args:
        stadium (int)

    Raises:
        ValueError: Occurred when stadium is not in [1, 2, ..., {NUM_STADIUMS}]
    """
    if (stadium < 1) or (NUM_STADIUMS < stadium):
        raise ValueError(
            f'Stadium must be between 1 and {NUM_STADIUMS}. '
            f'But {stadium} is given.'
        )


def validate_race(race: int):
    """Validate race no

    Args:
        race (int)

    Raises:
        ValueError: Occurred when race is not in [1, 2, ..., {NUM_RACES}].
    """
    if (race < 1) or (NUM_RACES < race):
        raise ValueError(
            f'Race must be between 1 and {NUM_RACES}. {race} is given.'
        )
