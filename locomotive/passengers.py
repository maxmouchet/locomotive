import json
from pathlib import Path

from attr import attrib, attrs

import cattr


class Passengers:
    def __init__(self, path=None):
        if path is None:
            path = self.default_path()
        self.path = Path(path).expanduser().absolute()
        if self.path.exists():
            self.passengers = [
                cattr.structure(x, Passenger) for x in json.load(open(self.path))
            ]
        else:
            self.passengers = []  # TODO: Default "dummy" passenger

    def __iter__(self):
        return self.passengers.__iter__()

    @classmethod
    def default_path(cls):
        return Path.home().joinpath(".locomotive", "passengers.json")

    def add(self, passenger):
        self.passengers.append(passenger)

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        obj = list(map(cattr.unstructure, self.passengers))
        json.dump(obj, open(self.path, "w"), indent=2)
        return self.path


@attrs
class Passenger:
    age = attrib()
    name = attrib()

    @classmethod
    def dummy(cls):
        return cls(age=26, name="Default Passenger")
