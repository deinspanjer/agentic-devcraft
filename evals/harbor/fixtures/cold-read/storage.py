_values: dict[str, str] = {}


def save(key: str, value: str) -> None:
    _values[key] = value


def save_batch(items: dict[str, str]) -> None:
    for key, value in items.items():
        save(key, value)
