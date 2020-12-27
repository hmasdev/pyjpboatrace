
class NoDataException(Exception):
    pass


class UnableActionException(Exception):
    pass


class LoginFailException(Exception):
    pass


class InsufficientDepositException(Exception):
    pass


class ZeroDepositException(InsufficientDepositException):
    pass


class VoteNotInTimeException(Exception):
    pass


class InactiveStadium(Exception):
    pass


class InactiveRace(Exception):
    pass
