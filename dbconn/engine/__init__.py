import subprocess

from dbconn.conf import Database
from dbconn import utils


def get_engine(db: Database):
    from dbconn.engine.mysql import MysqlEngine
    from dbconn.engine.postgres import PostgresEngine

    engines = {
        "mysql": MysqlEngine,
        "postgres": PostgresEngine,
    }
    default = "postgres"
    engine = engines.get(db.engine or default)
    if not engine:
        raise ValueError(f"Unsupported engine {db.engine}")

    return engine(db)


class Executable:
    def get_command(db: Database):
        raise NotImplementedError


class Engine:
    supported_executables: dict[str, Executable] = {}
    default_executable: Executable | None = None

    def __init__(self, db: Database):
        self.db = db

        self.executable = self.supported_executables.get(db.executable or self.default_executable)
        if not self.executable:
            raise ValueError(
                f"Unsupported executable {db.executable} for engine {self.__class__.__name__}"
            )

    def connect(self):
        # TODO: tunnel
        cmd = self.executable.get_command(self.db)

        print(f"\033[33mConnecting to {self.db}\033[0m")
        print(f"\033[36mCommand: {utils.format_command(cmd)}\033[0m")

        p = subprocess.Popen(cmd)
        p.wait()
