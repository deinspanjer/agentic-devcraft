def parse_port(value: str) -> int:
    """Return a valid TCP port number."""
    port = int(value)
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port
