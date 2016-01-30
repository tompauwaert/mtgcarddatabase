
class InvalidDataError(Exception):
    """
    Exception to be used when the expected data is in the wrong format,
    corrupted, or otherwise invalid.
    """
    pass


class DataUnavailable(Exception):
    """
    Exception to be used when the requested data is unavailable.
    """
    pass


class IllegalArgumentException(ValueError):
    """
    Exception to be used when an invalid argument has been passed.
    """
    pass
