#!/usr/bin/env python3
"""Enrich Cornucopia Mobile card mappings from generated MASTG and MASWE metadata."""

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from pathvalidate.argparse import validate_filepath_arg

MAX_YAML_FILE_SIZE_BYTES = 2 * 1024 * 1024
FILENAME_COMPONENT_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")


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


DEFAULT_SOURCE_DIR = Path(__file__).parent / "../source"
MAPPING_FIELDS = ("owasp_mastg", "owasp_mastg_know", "owasp_mastg_best", "owasp_maswe")


def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    """Parse source and output locations for one edition/version mapping set."""
    parser = argparse.ArgumentParser(description="Enrich Mobile card mappings with MASTG and MASWE metadata")
    parser.add_argument(
        "-e",
        "--edition",
        type=validate_filename_component,
        default="mobileapp",
        help="Cornucopia edition, for example mobileapp",
    )
    parser.add_argument(
        "-v", "--version", type=validate_filename_component, default="2.0", help="Cornucopia version, for example 2.0"
    )
    parser.add_argument("-s", "--source-dir", type=validate_filepath_arg, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("-i", "--input-path", type=validate_filepath_arg, help="Card mapping YAML to enrich")
    parser.add_argument("--mastg-path", type=validate_filepath_arg, help="Generated MASTG metadata YAML")
    parser.add_argument("--maswe-path", type=validate_filepath_arg, help="Generated MASWE metadata YAML")
    parser.add_argument(
        "-o", "--output-path", type=validate_filepath_arg, help="Enriched mapping YAML; defaults to input"
    )
    return parser.parse_args(input_args)


def validate_filename_component(value: str) -> str:
    """Allow only a single filename component for generated mapping names."""
    if not FILENAME_COMPONENT_PATTERN.fullmatch(value) or value in {".", ".."}:
        raise argparse.ArgumentTypeError("must contain only letters, digits, dots, underscores, and hyphens")
    return value


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML mapping or raise a clear error for invalid input."""
    if path.stat().st_size > MAX_YAML_FILE_SIZE_BYTES:
        raise ValueError(f"{path}: file exceeds {MAX_YAML_FILE_SIZE_BYTES} byte limit")
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeySafeLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    return data


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


def infer_mastg_mappings(card_id: str, test_ids: list[str], mastg_data: dict[str, Any]) -> dict[str, list[str]]:
    """Collect mappings inferred from available MASTG test metadata."""
    inferred: dict[str, list[str]] = {field: [] for field in MAPPING_FIELDS}
    for test_id in test_ids:
        if test_id == "-":
            continue
        test_mapping = mastg_data.get(test_id)
        if not isinstance(test_mapping, dict):
            logging.warning("%s: skipping MASTG test %r because it is absent from generated metadata", card_id, test_id)
            continue
        inferred["owasp_mastg"].append(test_id)
        for field in ("owasp_mastg_know", "owasp_mastg_best", "owasp_maswe"):
            inferred[field] = merge_unique(
                inferred[field], string_list(test_mapping.get(field), f"MASTG {test_id} {field}")
            )
    return inferred


def collect_maswe_references(
    card_id: str, weakness_ids: list[str], maswe_data: dict[str, Any]
) -> tuple[dict[str, str], dict[str, str]]:
    """Collect threat and attack descriptions for inferred MASWE weaknesses."""
    threats: dict[str, str] = {}
    attack_vectors: dict[str, str] = {}
    for weakness_id in weakness_ids:
        weakness_mapping = maswe_data.get(weakness_id)
        if not isinstance(weakness_mapping, dict):
            raise ValueError(f"{card_id}: MASWE {weakness_id!r} is missing from generated metadata")
        for field, destination in (("owasp_mas_threat", threats), ("owasp_mas_attack", attack_vectors)):
            references = weakness_mapping.get(field, {})
            if not isinstance(references, dict) or not all(
                isinstance(identifier, str) and isinstance(description, str)
                for identifier, description in references.items()
            ):
                raise ValueError(f"MASWE {weakness_id} {field}: expected identifier-to-description mapping")
            destination.update(references)
    return threats, attack_vectors


def enrich_card(card: dict[str, Any], mastg_data: dict[str, Any], maswe_data: dict[str, Any]) -> None:
    """Merge MASTG siblings and their MASWE threat and attack descriptions into one card."""
    card_id = card.get("id", "unknown card")
    test_ids = string_list(card.get("owasp_mastg"), f"{card_id} owasp_mastg")
    inferred = infer_mastg_mappings(card_id, test_ids, mastg_data)
    threats, attack_vectors = collect_maswe_references(card_id, inferred["owasp_maswe"], maswe_data)

    for field in MAPPING_FIELDS:
        card[field] = merge_unique(string_list(card.get(field), f"{card_id} {field}"), inferred[field])
    if threats:
        card["threat"] = threats
    if attack_vectors:
        card["attack_vector"] = attack_vectors


def enrich_mappings(
    mapping_data: dict[str, Any], mastg_data: dict[str, Any], maswe_data: dict[str, Any]
) -> dict[str, Any]:
    """Enrich every card mapping in a Mobile edition mapping document."""
    suits = mapping_data.get("suits")
    if not isinstance(suits, list):
        raise ValueError("Card mappings: expected suits list")
    for suit in suits:
        if not isinstance(suit, dict) or not isinstance(suit.get("cards"), list):
            raise ValueError("Card mappings: each suit must contain a cards list")
        for card in suit["cards"]:
            if not isinstance(card, dict):
                raise ValueError("Card mappings: each card must be a mapping")
            enrich_card(card, mastg_data, maswe_data)
    return mapping_data


def save_yaml_file(path: Path, data: dict[str, Any]) -> None:
    """Write enriched YAML with stable key order and safe zero-padded identifiers."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as output_file:
        yaml.dump(data, output_file, Dumper=LeadingZeroStringDumper, allow_unicode=True, sort_keys=False)


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


if __name__ == "__main__":
    main()
