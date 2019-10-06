from stage.motor import coil


class DriveScheme:
    """
    https://en.wikipedia.org/wiki/Stepper_motor#/media/File:Drive.png
    """
    @property
    def name(self):
        raise NotImplementedError

    @property
    def sequence(self):
        raise NotImplementedError


class FullStepDriveScheme(DriveScheme):
    name = "Full Step"
    sequence = [
        coil.State(1, 0, 0, 1),
        coil.State(1, 0, 0, 1),
        coil.State(1, 1, 0, 0),
        coil.State(1, 1, 0, 0),
        coil.State(0, 1, 1, 0),
        coil.State(0, 1, 1, 0),
        coil.State(0, 0, 1, 1),
        coil.State(0, 0, 1, 1),
    ]


class WaveDriveScheme(DriveScheme):
    name = "Wave"
    sequence = [
        coil.State(1, 0, 0, 0),
        coil.State(1, 0, 0, 0),
        coil.State(0, 1, 0, 0),
        coil.State(0, 1, 0, 0),
        coil.State(0, 0, 1, 0),
        coil.State(0, 0, 1, 0),
        coil.State(0, 0, 0, 1),
        coil.State(0, 0, 0, 1),
    ]


class HalfStepDriveScheme(DriveScheme):
    name = "Half Step"
    sequence = [
        coil.State(1, 0, 0, 1),
        coil.State(1, 0, 0, 0),
        coil.State(1, 1, 0, 0),
        coil.State(0, 1, 0, 0),
        coil.State(0, 1, 1, 0),
        coil.State(0, 0, 1, 0),
        coil.State(0, 0, 1, 1),
        coil.State(0, 0, 0, 1),
    ]
