#!/usr/bin/env python3

import os

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


def main():
    data = load_config()

    for db in data['databases']:
        db['password'] = db['password'].replace('\\', '\\\\').replace(':', '\\:')
        print('{host}:{port}:{database}:{user}:{password}'.format(**db))



if __name__ == '__main__':
    main()
