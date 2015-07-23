
class InvalidDataError(Exception):
    """
    Exception to be used when the expected data is in the wrong format,
    corrupted, or otherwise invalid.
    """
    pass


class DataUnavailable(Exception):
    """
    Exception to be used when the requested data is unavailabe.
    """
    pass