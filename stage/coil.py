from collections import namedtuple

from stage import iointerface

_LABELS = ['a1', 'b1', 'a2', 'b2']
State = namedtuple('State', _LABELS)
Pins = namedtuple("Pins", _LABELS)


class Coils:
    """
    Manages the coils needed to run a stepper motor
    """
    def __init__(
        # FIX: interface is a class whereas gpio is the actual driver - inconsistent with endstop init
            self, pins: Pins, interface: iointerface.OutputInterface, gpio):
        self._coils = [interface(pin, gpio) for pin in pins]
        self._state = None

    @property
    def coils(self):
        return self._coils

    def deactivate(self):
        for coil in self._coils:
            coil.deactivate()

    def set_state(self, state):
        self._state = state
        for coil, output in zip(self._coils, state):
            coil.activate() if output else coil.deactivate()
