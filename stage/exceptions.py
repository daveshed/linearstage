"""
Custom exceptions required by the stage package
"""

class BadConfigurationData(Exception):
    """
    Configuration is bad or missing data
    """

class OutOfRangeError(Exception):
    """
    Raised when the linear stage is requested to move outside of its allowed
    range.
    """
