#!/usr/bin/env python3

import os
import subprocess
import sys

from iterfzf import iterfzf
import yaml

# TODO: Dedupe
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

    return data

def connect(db):
    print('\033[33mConnecting to {id} ({host})\033[0m'.format(**db))
    cmd = [
        'psql',
        '-U', db['user'],
        '--host', db['host'],
        '--port', str(db['port']),
        '--db', db['database']
    ]
    print('\033[36mCommand: {}\033[0m'.format(' '.join(cmd)))
    p = subprocess.Popen(cmd)
    p.wait()

def main():
    data = load_config()
    databases = {d['id']: d for d in data['databases']}

    if (len(sys.argv) > 1):
        selected = sys.argv[1]
    else:
        selected = iterfzf(sorted(databases.keys()))

    connect(databases[selected])


if __name__ == '__main__':
    main()
