class BadConfigurationData(Exception):
    """
    Configuration is bad or missing data
    """
    pass

class OutOfRangeError(Exception):
    """
    Raised when the linear stage is requested to move outside of its allowed
    range.
    """
    pass