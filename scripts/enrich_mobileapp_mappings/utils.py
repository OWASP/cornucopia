from typing import Any


def merge_unique(existing: list[str], additions: list[str]) -> list[str]:
    """Append source-ordered additions without duplicating identifiers."""
    result = list(existing)
    for value in additions:
        if value not in result:
            result.append(value)
    return result


def string_list(value: Any, context: str) -> list[str]:
    """Validate an optional list of identifier strings."""
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{context}: expected a list of strings")
    return value
