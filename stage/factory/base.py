import abc


class StageFactoryBase(abc.ABC):

    @abc.abstractproperty
    def minimum_position(self):
        return

    @abc.abstractproperty
    def maximum_position(self):
        return

    @abc.abstractproperty
    def motor(self):
        return

    @abc.abstractproperty
    def end_stop(self):
        return
