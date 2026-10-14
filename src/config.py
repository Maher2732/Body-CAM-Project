import json
from pathlib import Path


CONFIG_PATH = Path("config.json")


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


config = load_config()