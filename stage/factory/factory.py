from stage.coil import Coils
from stage.coil import Pins
from stage.gpio import interface as iointerface


class Factory:

    @staticmethod
    def make_coils(
        pins: Pins, interface_type: iointerface.OutputInterface, gpio):
        outputs = (interface_type(pin, gpio) for pin in pins)
        return Coils(*outputs)
