from collections import namedtuple

from stage.gpio import interface as iointerface

_LABELS = ['a1', 'b1', 'a2', 'b2']
State = namedtuple('State', _LABELS)
Pins = namedtuple("Pins", _LABELS)


class Coils:
    """
    Manages the coils needed to run a stepper motor
    """
    def __init__(self, *outputs):
        self._state = None
        self._outputs = outputs

    @property
    def coils(self):
        return self._outputs

    def deactivate(self):
        for output in self._outputs:
            output.deactivate()

    def set_state(self, state):
        self._state = state
        for output, active in zip(self._coils, state):
            output.activate() if active else output.deactivate()
