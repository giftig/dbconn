from dataclasses import dataclass
import os

import yaml


@dataclass
class Database:
    id: str
    host: str
    port: int
    database: str
    user: str
    password: str | None
    engine: str | None = None
    executable: str | None = None
    tunnel: str | None = None

    def __str__(self):
        return f"{self.id} ({self.host})"


class Config:
    def __init__(self, databases):
        dbs = [Database(**d) for d in databases]
        self.databases = {d.id: d for d in dbs}

        if len(dbs) != len(self.databases):
            raise ValueError("One or more databases have duplicate IDs")


def load_config(config_file: str | None = None):
    data = None
    config_file = config_file or os.environ.get(
        "DBCONN_CONFIG_FILE", os.path.join(os.environ.get("HOME", "/"), ".dbconn/config.yaml")
    )

    with open(config_file, "r") as f:
        data = yaml.safe_load(f)

    return Config(**data)
