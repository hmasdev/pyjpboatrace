class NoDataException(Exception):
    pass


class RaceCancelledException(Exception):
    def __init__(self, msg=None):
        super().__init__(msg)


class UnableActionException(Exception):
    def __init__(self, msg=None):
        super().__init__(msg)


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


class UserInformationNotGivenException(Exception):
    pass
