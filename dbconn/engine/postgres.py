from dbconn.conf import Database
from dbconn.engine import Engine, Executable


class PsqlExecutable(Executable):
    def get_command(db: Database):
        return [
            "psql",
            "-U",
            db.user,
            "--host",
            db.host,
            "--port",
            str(db.port),
            "--db",
            db.database,
        ]


class PgcliExecutable(Executable):
    def get_command(db: Database):
        return [
            "pgcli",
            "-U",
            db.user,
            "--host",
            db.host,
            "--port",
            str(db.port),
            "--dbname",
            db.database,
        ]


class PostgresEngine(Engine):
    supported_executables = {
        "psql": PsqlExecutable,
        "pgcli": PgcliExecutable,
    }
    default_executable = "pgcli"
