from dbconn.conf import Database
from dbconn.engine import Engine, Executable


class MysqlExecutable(Executable):
    def get_command(db: Database):
        return [
            "mysql",
            "-u",
            db.user,
            "-h",
            db.host,
            f"--password={db.password}",
            "--port",
            str(db.port),
            f"--database={db.database}",
        ]


class MysqlEngine(Engine):
    supported_executables = {"mysql": MysqlExecutable}
    default_executable = "mysql"
