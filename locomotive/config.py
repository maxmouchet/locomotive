import json
from pathlib import Path

DEFAULT_CONFIG = {"locale": "en-US"}


class Config:
    def __init__(self, path=None):
        if path is None:
            path = self.default_path()
        self.path = Path(path).expanduser().absolute()
        if self.path.exists():
            self.config = {**DEFAULT_CONFIG, **json.load(self.path)}
        else:
            self.config = {**DEFAULT_CONFIG}

    @classmethod
    def default_path(cls):
        return Path.home().joinpath(".locomotive", "config.json")

    def init(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(self.config, open(self.path, "w"), indent=2)
        return self.path
