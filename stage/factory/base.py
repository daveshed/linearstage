#pylint: disable=missing-docstring
#pyling: enable=missing-docstring
import abc


class StageFactoryBase(abc.ABC):
    """
    The factory base class that provides necessary objects required to
    instantiate a Stage object.
    """
    @abc.abstractproperty
    def minimum_position(self):
        """The stage minimum position"""
        return

    @abc.abstractproperty
    def maximum_position(self):
        """The stage maximum position"""
        return

    @abc.abstractproperty
    def motor(self):
        """The motor to be used by the stage"""
        return

    @abc.abstractproperty
    def end_stop(self):
        """
        End stop object that is triggered when the stage reaches the end of
        its travel
        """
        return
