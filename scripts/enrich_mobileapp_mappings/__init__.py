#!/usr/bin/env python3
"""Enrich Cornucopia Mobile card mappings from generated MASTG and MASWE metadata."""

import sys
from pathlib import Path
from typing import Any

from .arguments import (
    DEFAULT_SOURCE_DIR,
    parse_arguments,
    validate_filename_component,
)
from .card import enrich_card
from .constants import MAPPING_FIELDS
from .document import enrich_mappings
from .masvs import infer_masvs_mappings
from .mastg import infer_mastg_mappings
from .maswe import collect_maswe_references
from .utils import merge_unique, string_list
from .yaml_loader import (
    UniqueKeySafeLoader,
    load_yaml_file as _load_yaml_file,
)
from .yaml_output import (
    LeadingZeroStringDumper,
    represent_list,
    represent_string,
    save_yaml_file,
)

MAX_YAML_FILE_SIZE_BYTES = 2 * 1024 * 1024

__all__ = [
    "DEFAULT_SOURCE_DIR",
    "LeadingZeroStringDumper",
    "MAPPING_FIELDS",
    "MAX_YAML_FILE_SIZE_BYTES",
    "UniqueKeySafeLoader",
    "collect_maswe_references",
    "enrich_card",
    "enrich_mappings",
    "infer_masvs_mappings",
    "infer_mastg_mappings",
    "load_yaml_file",
    "main",
    "merge_unique",
    "parse_arguments",
    "represent_list",
    "represent_string",
    "save_yaml_file",
    "string_list",
    "validate_filename_component",
]


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML mapping using the configured input size limit."""
    return _load_yaml_file(path, MAX_YAML_FILE_SIZE_BYTES)


def main() -> None:
    """Load generated metadata, enrich card mappings, and write the target YAML file."""
    args = parse_arguments(sys.argv[1:])
    source_dir = Path(args.source_dir).resolve()
    mapping_path = (
        Path(args.input_path).resolve()
        if args.input_path
        else source_dir / f"{args.edition}-mappings-{args.version}.yaml"
    )
    mastg_path = (
        Path(args.mastg_path).resolve() if args.mastg_path else source_dir / f"{args.edition}-mastg-{args.version}.yaml"
    )
    maswe_path = (
        Path(args.maswe_path).resolve() if args.maswe_path else source_dir / f"{args.edition}-maswe-{args.version}.yaml"
    )
    output_path = Path(args.output_path).resolve() if args.output_path else mapping_path
    save_yaml_file(
        output_path,
        enrich_mappings(load_yaml_file(mapping_path), load_yaml_file(mastg_path), load_yaml_file(maswe_path)),
    )
