#!/usr/bin/env python3

import os
import subprocess
import sys

from iterfzf import iterfzf
import yaml


EXEC_PSQL = 'psql'
EXEC_PGCLI = 'pgcli'
EXEC_MYSQL = 'mysql'

SUPPORTED_EXECS = {EXEC_PSQL, EXEC_PGCLI, EXEC_MYSQL}


class Database:
    def __init__(self, id, host, port, database, user, password, executable=None):
        self.id = id
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.executable = executable

    def __str__(self):
        return f'{self.id} ({self.host})'


class Config:
    def __init__(self, databases, executable=EXEC_PSQL):
        dbs = [Database(**d) for d in databases]
        self.databases = {d.id: d for d in dbs}

        if len(dbs) != len(self.databases):
            raise ValueError('One or more databases have duplicate IDs')

        self.executable = executable

        if self.executable not in SUPPORTED_EXECS:
            raise ValueError(f'Executable {self.executable} not supported!')


def load_config():
    data = None
    config_file = os.environ.get(
        'POSTGRES_SELECTOR_CONFIG_FILE',
        os.path.join(
            os.environ.get('HOME', '/'),
            '.psql-selector/postgres.yaml'
        )
    )

    with open(config_file, 'r') as f:
        data = yaml.safe_load(f)

    return Config(**data)


def _format_command(cmd):
    """Apply rudimentary password masking and present the command"""
    pieces = []

    for p in cmd:
        if p.startswith("--password="):
            pieces.append("--password=*******")
            continue

        pieces.append(p)

    return " ".join(pieces)


def get_command(db, default_executable):
    executable = db.executable or default_executable

    if executable == EXEC_PSQL:
        return [
            'psql',
            '-U', db.user,
            '--host', db.host,
            '--port', str(db.port),
            '--db', db.database
        ]

    if executable == EXEC_PGCLI:
        return [
            'pgcli',
            '-U', db.user,
            '--host', db.host,
            '--port', str(db.port),
            '--dbname', db.database
        ]

    if executable == EXEC_MYSQL:
        # TODO: Provide password via a my.cnf file or some other way, cli isn't secure
        return [
            'mysql',
            '-u', db.user,
            '-h', db.host,
            f'--password={db.password}',
            '--port', str(db.port),
            f'--database={db.database}'
        ]

    raise ValueError(f'Executable {executable} not supported!')


def connect(db, executable):
    cmd = get_command(db, executable)

    print(f'\033[33mConnecting to {db}\033[0m')
    print(f'\033[36mCommand: {_format_command(cmd)}\033[0m')

    p = subprocess.Popen(cmd)
    p.wait()


def main():
    conf = load_config()
    selected = (
        sys.argv[1]
        if len(sys.argv) > 1 else
        iterfzf(sorted(conf.databases.keys()))
    )
    connect(conf.databases[selected], conf.executable)


if __name__ == '__main__':
    main()
