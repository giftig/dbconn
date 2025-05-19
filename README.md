# Database cli selector

## Purpose

Lightweight cli for easily configuring and connecting to multiple different Postgres or MySQL databases.
Configure your various databases as YAML and use fzf to select which one you want to connect to.

Supports `psql` and `pgcli` for postgres, and the `mysql` cli for mysql (you'll need to install these cli
tools yourself).

## Config file example

```yaml
databases:
  - id: pg1
    host: "foo-bar-baz.21272834.eu-west-1.rds.amazonaws.com"
    port: 5432
    database: database_123
    user: admin
    password: password1

  - id: pg2
    executable: psql
    host: "foo-baz-bar.21272854.eu-west-1.rds.amazonaws.com"
    port: 5432
    database: database_321
    user: root
    password: password2

  - id: mysql1
    engine: mysql
    host: "foo-baz-bar.21272666.eu-west-1.rds.amazonaws.com"
    port: 3306
    database: database_666
    user: root
    password: password2

```

## Quickstart

Use `dbconn --pgpass > ~/.pgpass` to generate a pgpass file for your postgres databases, based on your yaml
config. You can regenerate this whenever you update your database list. Make sure you chmod the pgpass file to
`0600`.

Use `dbconn {id}` to connect to a database by ID, or `dbconn` to present a summary of configured
databases to search for.
