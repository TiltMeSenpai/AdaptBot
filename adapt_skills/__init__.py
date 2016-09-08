import os
import inspect
import pathlib
import json
from .skills import Skill

filename = inspect.stack()[0][1][:-11]
__all__ = []
skills = {}

for file in os.listdir(filename):
    if pathlib.Path(filename, file, "config.json").exists():
        with pathlib.Path(filename, file, "config.json").open() as config:
            skills[file] = json.load(config)
        __all__.append(file)
