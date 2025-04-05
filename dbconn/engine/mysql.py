from dbconn.conf import Database
from dbconn.engine import Engine, Executable


class MysqlExecutable(Executable):
    def get_command(db: Database, host: str | None = None, port: int | None = None):
        return [
            "mysql",
            "-u",
            db.user,
            "-h",
            host or db.host,
            f"--password={db.password}",
            "--port",
            str(port or self.port),
            f"--database={db.database}",
        ]


class MysqlEngine(Engine):
    supported_executables = {"mysql": MysqlExecutable}
    default_executable = "mysql"
    default_port = 3306
