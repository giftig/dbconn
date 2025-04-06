#!/usr/bin/env python3

import argparse
import sys

from iterfzf import iterfzf

from dbconn import conf
from dbconn.engine import get_engine


def gen_pgpass(cfg: conf.Config):
    for db in cfg.databases.values():
        if db.engine is not None and db.engine != "postgres":
            continue

        password = db.password.replace("\\", "\\\\").replace(":", "\\:")
        print(f"{db.host}:{db.port}:{db.database}:{db.user}:{password}")


def main():
    parser = argparse.ArgumentParser("dbconn")
    parser.add_argument(
        "-p",
        "--pgpass",
        action="store_true",
        dest="gen_pgpass",
        help=(
            "Print a pgpass file corresponding to the database config and exit, instead of "
            "connecting to a database"
        ),
    )
    parser.add_argument(
        "-c",
        "--config-file",
        help="Use the given config file. You can also set this via the DBCONN_CONFIG_FILE env var",
    )
    args = parser.parse_args()

    cfg = conf.load_config(args.config_file)

    if args.gen_pgpass:
        return gen_pgpass(cfg)

    selected = sys.argv[1] if len(sys.argv) > 1 else iterfzf(sorted(cfg.databases.keys()))
    db = cfg.databases[selected]

    get_engine(db).connect()


if __name__ == "__main__":
    main()
