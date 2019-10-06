import logging

_LOGGER = logging.getLogger("MOCK")

class MockMotor:

    def __init__(self, fake_track):
        self.deactivated = False
        self._fake_track = fake_track

    def forward(self, steps: int):
        _LOGGER.info("Mock motor forward %d steps", steps)
        self._fake_track.position += steps

    def backward(self, steps: int):
        _LOGGER.info("Mock motor backward %d steps", steps)
        self._fake_track.position -= steps

    def deactivate(self):
        self.deactivated = True
