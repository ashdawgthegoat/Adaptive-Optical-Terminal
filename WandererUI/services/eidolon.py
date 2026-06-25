import json
import uuid
from datetime import datetime
from pathlib import Path


class Eidolon:

    ROOT = Path.home() / "Wanderer"

    @classmethod
    def create_observation(
        cls,
        category,
        name
    ):

        observation_path = (
            cls.ROOT /
            category /
            name
        )

        if observation_path.exists():
            return False

        observation_path.mkdir(
            parents=True
        )

        (
            observation_path /
            "media"
        ).mkdir()

        (
            observation_path /
            "metadata"
        ).mkdir()

        (
            observation_path /
            "exports"
        ).mkdir()

        (
            observation_path /
            "notes.md"
        ).touch()

        observation = {

            "id": str(uuid.uuid4()),

            "name": name,

            "category": category,

            "created": datetime.now().isoformat(),

            "last_modified": datetime.now().isoformat()

        }

        with open(

            observation_path /
            "observation.json",

            "w"

        ) as file:

            json.dump(

                observation,

                file,

                indent=4

            )

        return True
    
    @classmethod
    def get_observations(
        cls,
        category
    ):

        category_path = (
            cls.ROOT /
            category
        )

        if not category_path.exists():
            return []

        observations = []

        for item in sorted(
            category_path.iterdir()
        ):

            if item.is_dir():

                observations.append(
                    item.name
                )

        return observations

    @classmethod
    def open_observation(
        cls,
        category,
        name
    ):

        observation_path = (
            cls.ROOT /
            category /
            name
        )

        json_path = (
            observation_path /
            "observation.json"
        )

        notes_path = (
            observation_path /
            "notes.md"
        )

        if not json_path.exists():
            return None

        with open(
            json_path,
            "r"
        ) as file:

            observation = json.load(file)

        if notes_path.exists():

            with open(
                notes_path,
                "r"
            ) as file:

                observation["notes"] = (
                    file.read()
                )

        else:

            observation["notes"] = ""

        observation["root"] = (
            str(observation_path)
        )

        return observation