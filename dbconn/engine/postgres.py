from dbconn.conf import Database
from dbconn.engine import Engine, Executable


class PsqlExecutable(Executable):
    def get_command(self, db: Database, host: str | None = None, port: int | None = None):
        return [
            "psql",
            "-U",
            db.user,
            "--host",
            host or db.host,
            "--port",
            str(port),
            "--db",
            db.database,
        ]


class PgcliExecutable(Executable):
    def get_command(self, db: Database, host: str | None = None, port: int | None = None):
        return [
            "pgcli",
            "-U",
            db.user,
            "--host",
            host or db.host,
            "--port",
            str(port),
            "--dbname",
            db.database,
        ]


class PostgresEngine(Engine):
    supported_executables = {
        "psql": PsqlExecutable,
        "pgcli": PgcliExecutable,
    }
    default_executable = "pgcli"
    default_port = 5432
