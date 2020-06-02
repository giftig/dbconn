# Postgres management utils

## Purpose

Suite of tools for connecting to various different postgres databases

## Config file example

```yaml
databases:
  - id: db1
    host: "foo-bar-baz.21272834.eu-west-1.rds.amazonaws.com"
    port: 5432
    database: database_123
    user: admin
    password: password1

  - id: db2
    host: "foo-baz-bar.21272854.eu-west-1.rds.amazonaws.com"
    port: 5432
    database: database_321
    user: root
    password: password2

```

## Quickstart

Use `gen-pgpass.py > ~/.pgpass` to generate a pgpass file based on your yaml config. This will be
used by psql to read appropriate passwords. Make sure you chmod the pgpass file to `0600`.

Use `pgconn {id}` to connect to a postgres database by ID, or `pgconn` to present a summary of configured
databases to search for.
