import os
from typing import Any

from pydantic import BaseModel, ValidationError, field_validator
import yaml


class Tunnel(BaseModel):
    host: str
    port: int = 22
    user: str | None = None
    password: str | None = None
    pkey: str | None = None
    pkey_password: str | None = None


class Database(BaseModel):
    id: str
    host: str
    database: str
    user: str
    password: str | None = None
    port: int | None = None
    engine: str | None = None
    executable: str | None = None
    executable_options: dict = {}
    tunnel: Tunnel | None = None

    def __str__(self):
        return f"{self.id} ({self.host})"


class Config(BaseModel):
    databases: dict[str, Database]

    @field_validator("databases", mode="before")
    @classmethod
    def database_dict(cls, v: Any) -> dict[str, Database]:
        if not isinstance(v, list):
            raise ValidationError("Expected list of databases")

        dbs = [Database(**d) for d in v]
        by_id = {d.id: d for d in dbs}

        if len(dbs) != len(by_id):
            raise ValidationError("One or more databases have duplicate IDs")

        return by_id


def load_config(config_file: str | None = None):
    data = None
    config_file = config_file or os.environ.get(
        "DBCONN_CONFIG_FILE", os.path.join(os.environ.get("HOME", "/"), ".dbconn/config.yaml")
    )

    with open(config_file, "r") as f:
        data = yaml.safe_load(f)

    return Config(**data)
