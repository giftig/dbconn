def format_command(cmd):
    """Apply rudimentary password masking and present the command"""
    pieces = []

    for p in cmd:
        if p.startswith("--password="):
            pieces.append("--password=*******")
            continue

        pieces.append(p)

    return " ".join(pieces)
