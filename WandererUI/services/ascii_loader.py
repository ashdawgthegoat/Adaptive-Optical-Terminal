from pathlib import Path


ASCII_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    / "assets"
    / "ascii"
)


def load_ascii(name):

    filepath = (
        ASCII_DIR
        / f"{name}.txt"
    )

    if not filepath.exists():

        return (
            f"[ Missing ASCII: {name} ]"
        )

    return filepath.read_text(
        encoding="utf-8"
    )