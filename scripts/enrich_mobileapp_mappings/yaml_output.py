import re
from pathlib import Path
from typing import Any

import yaml


class LeadingZeroStringDumper(yaml.SafeDumper):
    """YAML dumper that preserves zero-padded identifiers as strings."""


def represent_string(dumper: LeadingZeroStringDumper, value: str) -> yaml.ScalarNode:
    """Use single quotes for digit-only strings that start with zero."""
    style = "'" if re.fullmatch(r"0\d+", value) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


def represent_list(dumper: LeadingZeroStringDumper, value: list[Any]) -> yaml.SequenceNode:
    """Keep scalar lists inline while preserving block layout for cards and suits."""
    return dumper.represent_sequence(
        "tag:yaml.org,2002:seq", value, flow_style=all(not isinstance(item, (dict, list)) for item in value)
    )


LeadingZeroStringDumper.add_representer(str, represent_string)
LeadingZeroStringDumper.add_representer(list, represent_list)


def save_yaml_file(path: Path, data: dict[str, Any]) -> None:
    """Write enriched YAML with stable key order and safe zero-padded identifiers."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as output_file:
        yaml.dump(data, output_file, Dumper=LeadingZeroStringDumper, allow_unicode=True, sort_keys=False)
