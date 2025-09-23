class BasePyJPBoatraceException(Exception):
    """Base class for all pyjpboatrace-specific exceptions."""
    pass


class NoDataException(BasePyJPBoatraceException):
    pass


class RaceCancelledException(BasePyJPBoatraceException):
    def __init__(self, msg=None):
        super().__init__(msg)


class UnableActionException(BasePyJPBoatraceException):
    def __init__(self, msg=None):
        super().__init__(msg)


class LoginFailException(BasePyJPBoatraceException):
    pass


class InsufficientDepositException(BasePyJPBoatraceException):
    pass


class ZeroDepositException(InsufficientDepositException):
    pass


class VoteNotInTimeException(BasePyJPBoatraceException):
    pass


class InactiveStadium(BasePyJPBoatraceException):
    pass


class InactiveRace(BasePyJPBoatraceException):
    pass


class UserInformationNotGivenException(BasePyJPBoatraceException):
    pass


class UnexpectedException(BasePyJPBoatraceException):
    pass


__all__ = [
    "BasePyJPBoatraceException",
    "NoDataException",
    "RaceCancelledException",
    "UnableActionException",
    "LoginFailException",
    "InsufficientDepositException",
    "ZeroDepositException",
    "VoteNotInTimeException",
    "InactiveStadium",
    "InactiveRace",
    "UserInformationNotGivenException",
    "UnexpectedException",
]
