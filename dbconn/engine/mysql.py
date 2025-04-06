from dbconn.conf import Database
from dbconn.engine import Engine, Executable


class MysqlExecutable(Executable):
    def __init__(self, prompt: str | None = None):
        self.prompt = prompt

    def get_command(self, db: Database, host: str | None = None, port: int | None = None):
        cmd = [
            "mysql",
            "-u",
            db.user,
            "-h",
            host or db.host,
            f"--password={db.password}",
            "--port",
            str(port),
            f"--database={db.database}",
        ]
        if self.prompt:
            cmd.append(f"--prompt={self.prompt}")

        return cmd


class MycliExecutable(Executable):
    def __init__(self, prompt: str | None = None):
        self.prompt = prompt

    def get_command(self, db: Database, host: str | None = None, port: int | None = None):
        cmd = [
            "mycli",
            "-u",
            db.user,
            "-h",
            host or db.host,
            f"--password={db.password}",
            "--port",
            str(port),
            f"--database={db.database}",
        ]
        if self.prompt:
            cmd.append(f"--prompt={self.prompt}")

        return cmd


class MysqlEngine(Engine):
    supported_executables = {"mysql": MysqlExecutable, "mycli": MycliExecutable}
    default_executable = "mycli"
    default_port = 3306
