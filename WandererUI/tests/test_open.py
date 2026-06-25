from services.eidolon import Eidolon

observation = Eidolon.open_observation(
    "Astronomy",
    "Jupiter"
)

print(observation)