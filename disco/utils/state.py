import os
import json

from .logger import init_logger


class State:
    def __init__(self, name, state_path, default=None, refresh_before_read=True):
        self.data = {}
        self.name = name
        self.refresh_before_read = refresh_before_read
        self.state_filename = os.path.join(state_path, f"{self.name}.json")
        self.default = default
        self.logger = init_logger()

        self.load()
        self.logger.info(f"loaded state from {self.state_filename}")


    def load(self):
        try:
            with open(self.state_filename, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}
            self.save()
        # except json.JSONDecodeError:
        #     self.data = {}
        #     self.save()

        return self.data

    def save(self):
        filename = os.path.expanduser(self.state_filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.data, f)

    def keys(self):
        return self.data.keys()

    def __getitem__(self, key):
        try:
            if self.refresh_before_read:
                self.load()
            return self.data[key]
        except KeyError:
            self.__setitem__(key, self.default)
            return self.default

    def __setitem__(self, key, value):
        self.data[key] = value

        # automatically save
        self.save()
