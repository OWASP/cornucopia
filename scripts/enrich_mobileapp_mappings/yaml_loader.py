from pathlib import Path
from typing import Any

import yaml


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects ambiguous duplicate mapping keys."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"Duplicate YAML key: {key!r}")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def load_yaml_file(path: Path, max_size_bytes: int) -> dict[str, Any]:
    """Load a YAML mapping or raise a clear error for invalid input."""
    if path.stat().st_size > max_size_bytes:
        raise ValueError(f"{path}: file exceeds {max_size_bytes} byte limit")
    # The custom loader inherits SafeLoader and adds duplicate-key rejection.
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeySafeLoader)  # nosec B506
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    return data
