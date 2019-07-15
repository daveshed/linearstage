"""
Defines the state of coils required by the motor
"""
from collections import namedtuple

State = namedtuple('State', 'a1, b1, a2, b2')


class Coils:
    def __init__(self, a1, b1, a2, b2):
        self._coils = [a1, b1, a2, b2]
    
    def deactivate(self):
        for coil in self._coils:
            coil.off()

    def set_state(self, state):
        for coil in self._coils:
            output = getattr(state, coil.label)
            if output:
                coil.on()
            else:
                coil.off()
