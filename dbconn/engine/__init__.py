import subprocess

import sshtunnel

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
    def get_command(db: Database, host: str | None = None, port: int | None = None):
        raise NotImplementedError


class Engine:
    supported_executables: dict[str, Executable] = {}
    default_executable: Executable | None = None
    default_port: int = 0

    def __init__(self, db: Database):
        self.db = db

        self.executable = self.supported_executables.get(db.executable or self.default_executable)
        if not self.executable:
            raise ValueError(
                f"Unsupported executable {db.executable} for engine {self.__class__.__name__}"
            )

    @property
    def port(self) -> int:
        """Get the DB port; override this per engine to define a fallback if it's not in db conf"""
        return self.db.port or self.default_port

    def _connect(self, host: str | None = None, port: int | None = None):
        cmd = self.executable.get_command(self.db, host, port)

        print(f"\033[33mConnecting to {self.db}\033[0m")
        print(f"\033[36mCommand: {utils.format_command(cmd)}\033[0m")

        p = subprocess.Popen(cmd)
        p.wait()

    def connect(self):
        if not self.db.tunnel:
            return self._connect()

        tun = self.db.tunnel
        free_port = utils.get_free_port()

        with sshtunnel.open_tunnel(
            (tun.host, tun.port or 22),
            ssh_username=tun.user,
            ssh_password=tun.password,
            ssh_pkey=tun.pkey,
            ssh_private_key_password=tun.pkey_password,
            remote_bind_address=(self.db.host, self.port),
            local_bind_address=("0.0.0.0", free_port),
        ):
            print(
                f"\033[32mTunnelling 0.0.0.0:{free_port} -> {self.db.host}:{self.port} "
                f"via {tun.host}\033[0m"
            )
            self._connect("127.0.0.1", free_port)
