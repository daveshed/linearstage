"""Error definitions for the linear stage"""

class OutOfRangeError(Exception):
    """
    Raised when the linear stage is requested to move outside of its allowed
    range.
    """
