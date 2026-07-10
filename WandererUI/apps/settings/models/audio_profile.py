from dataclasses import dataclass


# ==========================================================
# Audio Profile Model
#
# Represents the state of a single audio device.
#
#   name   — Display name of the audio profile.
#   device — System audio device identifier.
#   volume — Volume level from 0 to 100.
#   muted  — Whether the device is muted.
# ==========================================================


@dataclass
class AudioProfile:

    name: str
    device: str
    volume: int = 50
    muted: bool = False
