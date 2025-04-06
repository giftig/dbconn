from dbconn.conf import Database
from dbconn.engine import Engine, Executable


class MysqlExecutable(Executable):
    def __init__(self, prompt_text: str | None = None):
        self.prompt_text = prompt_text

    def get_command(self, db: Database, host: str | None = None, port: int | None = None):
        cmd = [
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
        if self.prompt_text:
            cmd.append(f"--prompt={self.prompt_text}> ")

        return cmd


class MysqlEngine(Engine):
    supported_executables = {"mysql": MysqlExecutable}
    default_executable = "mysql"
    default_port = 3306
