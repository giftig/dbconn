import random
import socketserver


def format_command(cmd):
    """Apply rudimentary password masking and present the command"""
    pieces = []

    for p in cmd:
        if p.startswith("--password="):
            pieces.append("--password=*******")
            continue

        pieces.append(p)

    return " ".join(pieces)


def get_free_port() -> int:
    with socketserver.TCPServer(("localhost", 0), None) as s:
        return s.server_address[1]
